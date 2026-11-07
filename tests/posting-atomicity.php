<?php
declare(strict_types=1);
namespace Chwezi\Finance\Posting;
// Synthetic dependency doubles. Only PDO SQLite :memory: is used.
use PDO;
class PostingRejected extends \RuntimeException {}
class PostingResult { public function __construct(public int $journalId) {} }
class CurrentUser { public int $id = 1; public string $roleContext = 'Test'; public function hasRole(string $r): bool { return true; } }
class CoaRepository { public string $rule='allowed'; public function byCode(string $c): object { return (object)['directPosting'=>$this->rule, 'evidenceRequired'=>'always']; } }
class PeriodStateRepository { public function stateFor(...$a): string { return 'open'; } }
class TaxCodeRepository {}
class SourceRegisterRepository {}
class PostingCommand {
 public int $entityId=1; public int $bookId=1; public \DateTimeImmutable $date;
 public string $sourceDocumentRef='TEST-INVOICE'; public string $idempotencyKey='TEST-KEY';
 public array $evidenceRefs=['TEST-EVIDENCE']; public array $lines;
 public function __construct() { $this->date=new \DateTimeImmutable('2026-11-07');
  $this->lines=[new JournalLine('TEST-CASH',100,0),new JournalLine('TEST-AR',0,100)]; }
 public function payloadHash(): string { return hash('sha256',serialize($this->lines)); }
}
class JournalLine {
 public string $currency='TEST'; public ?string $taxCode=null; public array $dimensions=[];
 public string $description='synthetic'; public string $sourceLineRef='TEST-LINE';
 public function __construct(public string $accountCode,public int $debit,public int $credit) {}
}
class AuditLog {
 public bool $fail=false; public bool $failAfter=false;
 public function __construct(private PDO $db) {}
 public function record(...$args): void {
  if($this->fail) throw new \RuntimeException('injected audit failure');
  $this->db->prepare('INSERT INTO audit VALUES (?)')->execute([$args['action']]);
  if($this->failAfter) throw new \RuntimeException('injected after audit insert');
 }
}
class IdempotencyStore {
 public bool $fail=false; public bool $failAfter=false;
 public function __construct(private PDO $db) {}
 public function lookup(string $key): ?object {
  $s=$this->db->prepare('SELECT * FROM idem WHERE key=?');$s->execute([$key]);$r=$s->fetch(PDO::FETCH_ASSOC);
  return $r ? (object)['payloadHash'=>$r['hash'],'result'=>new PostingResult((int)$r['journal'])] : null;
 }
 public function store(string $key,string $hash,PostingResult $result): void {
  if($this->fail) throw new \RuntimeException('injected idempotency failure');
  $this->db->prepare('INSERT INTO idem VALUES (?,?,?)')->execute([$key,$hash,$result->journalId]);
  if($this->failAfter) throw new \RuntimeException('injected after idempotency insert');
 }
}
require __DIR__.'/../skills/finance-accounting/accounting-engine/references/chwezi-finance-engine-skeletons/php-mysql/posting-service-skeleton.php';
function check(bool $value,string $message): void { if(!$value) throw new \RuntimeException($message); }
function fixture(): array {
 $db=new PDO('sqlite::memory:',null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
 $db->sqliteCreateFunction('NOW',fn()=> '2026-11-07 00:00:00');
 $db->exec('CREATE TABLE journal_headers(id INTEGER PRIMARY KEY,entity_id,book_id,date,period,source_document,idempotency_key UNIQUE,actor_user_id,actor_role,posting_service_version,status,created_at);
 CREATE TABLE journal_lines(journal_id,account_code,debit,credit,currency,tax_code,dimensions_json,description,source_line_ref);
 CREATE TABLE audit(action); CREATE TABLE idem(key PRIMARY KEY,hash,journal);');
 $audit=new AuditLog($db);$idem=new IdempotencyStore($db);$coa=new CoaRepository;
 $service=new PostingService($db,$coa,new PeriodStateRepository,new TaxCodeRepository,new SourceRegisterRepository,$audit,$idem,new CurrentUser);
 return [$db,$audit,$idem,$service,$coa];
}
foreach(['audit-before','audit-after','idempotency-before','idempotency-after'] as $failure) {
 [$db,$audit,$idem,$service]=fixture();
 try {
  $target=str_starts_with($failure,'audit')?$audit:$idem;
  if(str_ends_with($failure,'after')) $target->failAfter=true; else $target->fail=true;
  try { $service->post(new PostingCommand);throw new \LogicException('injection did not fail'); }
  catch(\LogicException $e) { throw $e; } catch(\RuntimeException $e) {}
  foreach(['journal_headers','journal_lines','audit','idem'] as $table)
   check((int)$db->query("SELECT count(*) FROM $table")->fetchColumn()===0,"$failure failure left $table committed");
  check(!$db->inTransaction(),'transaction leaked');
  $audit->fail=$idem->fail=$audit->failAfter=$idem->failAfter=false;
  $result=$service->post(new PostingCommand);
  $replay=$service->post(new PostingCommand);
  check($result->journalId===$replay->journalId,'replay changed result');
  foreach(['journal_headers'=>1,'journal_lines'=>2,'audit'=>1,'idem'=>1] as $table=>$count)
   check((int)$db->query("SELECT count(*) FROM $table")->fetchColumn()===$count,"retry count mismatch: $table");
  check((int)$db->query('SELECT sum(debit-credit) FROM journal_lines')->fetchColumn()===0,'unbalanced journal');
  echo "PASS $failure rollback, retry, same-key replay and balance\n";
 } finally { unset($target,$service,$audit,$idem,$db); }
}

foreach (['unbalanced','unauthorised-account','missing-evidence','missing-key'] as $case) {
 [$db,$audit,$idem,$service,$coa]=fixture();
 try {
  $cmd=new PostingCommand;
  if($case==='missing-key') $cmd->idempotencyKey=' ';
  if($case==='unbalanced') $cmd->lines[0]->debit=99;
  if($case==='unauthorised-account') $coa->rule='system-only';
  if($case==='missing-evidence') $cmd->evidenceRefs=[];
  $rejected=false;
  try {$service->post($cmd);} catch(PostingRejected $e) {$rejected=true;}
  check($rejected,"$case was not rejected");
  foreach(['journal_headers','journal_lines','audit','idem'] as $table)
   check((int)$db->query("SELECT count(*) FROM $table")->fetchColumn()===0,"$case mutated $table");
  echo "PASS $case rejected without ledger mutation\n";
 } finally {unset($service,$audit,$idem,$coa,$db);}
}

[$db,$audit,$idem,$service]=fixture();
try {
 $original=$service->post(new PostingCommand);
 $changed=new PostingCommand; $changed->lines[0]->debit=200; $changed->lines[1]->credit=200;
 $rejected=false;
 try {$service->post($changed);} catch(PostingRejected $e) {$rejected=true;}
 check($rejected,'changed payload not rejected');
 check((int)$db->query('SELECT count(*) FROM journal_headers')->fetchColumn()===1,'changed payload reposted');
 check((int)$db->query('SELECT count(*) FROM journal_lines')->fetchColumn()===2,'changed payload added lines');
 check((int)$db->query('SELECT count(*) FROM idem')->fetchColumn()===1,'changed payload changed key count');
 check((int)$db->query("SELECT count(*) FROM audit WHERE action='reject-idempotency-replay'")->fetchColumn()===1,'rejection audit missing');
 check($service->post(new PostingCommand)->journalId===$original->journalId,'rejection damaged original result');
 echo "PASS changed-payload rejection audit with original posting retained\n";
} finally {unset($original,$changed,$service,$audit,$idem,$db);}

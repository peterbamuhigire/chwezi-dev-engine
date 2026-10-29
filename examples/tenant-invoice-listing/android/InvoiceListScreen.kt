package com.example.invoices

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

sealed interface InvoiceListState {
    data object Loading : InvoiceListState
    data object Denied : InvoiceListState
    data class Failed(val message: String) : InvoiceListState
    data class Ready(val invoices: List<InvoiceRow>) : InvoiceListState
}

data class InvoiceRow(
    val id: String,
    val number: String,
    val customer: String,
    val currency: String,
    val amountMinor: String,
)

@Composable
fun InvoiceListScreen(
    state: InvoiceListState,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier,
) {
    when (state) {
        InvoiceListState.Loading -> Column(
            modifier.fillMaxSize(), verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally,
        ) { CircularProgressIndicator(); Text("Loading invoices") }
        InvoiceListState.Denied -> Text("You do not have access to invoices.", modifier)
        is InvoiceListState.Failed -> Column(modifier) {
            Text("Invoices could not be loaded.", color = MaterialTheme.colorScheme.error)
            Button(onClick = onRetry) { Text("Try again") }
        }
        is InvoiceListState.Ready -> if (state.invoices.isEmpty()) {
            Text("No invoices found.", modifier)
        } else {
            LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp), modifier = modifier) {
                items(state.invoices, key = InvoiceRow::id) { invoice ->
                    Column {
                        Text(invoice.number, style = MaterialTheme.typography.titleMedium)
                        Text(invoice.customer)
                        Text("${invoice.currency} ${invoice.amountMinor} minor units")
                    }
                }
            }
        }
    }
}

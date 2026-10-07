final class PagamentoLocal implements ConsultaPagamento {
    public StatusPagamento consultar(Pedido pedido) {
        return pedido.pagamento();
    }
}

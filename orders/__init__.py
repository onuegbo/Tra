from django.utils.translation import pgettext_lazy


class OrderStatus:
    OPEN = 'ouvert'
    CLOSED = 'fermer'

    CHOICES = [
        (OPEN, pgettext_lazy('order status', 'Open')),
        (CLOSED, pgettext_lazy('order status', 'Closed'))]


class GroupStatus:
    NEW = 'nouveau'
    CANCELLED = 'annuler'
    SHIPPED = 'shipped'

    CHOICES = [
        (NEW, pgettext_lazy('group status', 'Processing')),
        (CANCELLED, pgettext_lazy('group status', 'Cancelled')),
        (SHIPPED, pgettext_lazy('group status', 'Shipped'))]
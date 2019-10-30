from django.shortcuts import render , redirect , get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from core.forms import *
from core.models import *
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.http import HttpResponse , JsonResponse

from core.models import Immobile
from django.db.models import Q

def index ( request ) :
    return render ( request , 'index.html')

def login ( request ) :
    if request.method == 'GET' :
        return render ( request , 'login.html' )
    if request.method == 'POST' :
        if request.POST.get ( 'password' ) != '' and request.POST.get ( 'username' ) != '' :
            utente = Users.objects.filter ( username=request.POST.get ( 'username' ) )
            if len ( utente ) == 1 :
                if utente [ 0 ].password == request.POST.get ( 'password' ) :
                    request.session [ 'username' ] = request.POST.get ( 'username' )
                    request.session [ 'user_id' ] = utente.first ().pk
                    return redirect ( 'index' )
        return render ( request , 'login.html' , { 'msg' : 'I dati inseriti non sono corretti.' } )

def logout ( request ) :
    request.session.flush ()
    return redirect ( '/login/' )

def view_vendita(request):
    return render(request,'immobili.html')

def view_rubrica ( request ) :
    return render ( request , 'rubrica.html')

def amministrazione ( request ) :
    if request.method == 'POST' :
        formFascia = FormFascia ( request.POST )
        if formFascia.is_valid () :
            formFascia.save ()
            msg = 'Immobile inserito con successo'
            formFascia = FormFascia ()
            return redirect ( 'amministrazione' )
    else :
        formFascia = FormFascia ()
    return render ( request , 'amministrazione.html' , { 'formFascia' : formFascia } )


def aggiungi_cliente ( request ) :
    if request.method == 'POST' :
        form = FormCliente ( request.POST )
        if form.is_valid():
            form.save ()
            msg = 'Cliente inserito con successo'
        return render(request, 'rubrica.html', {'msg':msg})
        # return render ( request , 'form_cliente.html' , { 'form' : form } )
    else :
        form = FormCliente ()
    return render ( request , 'form_cliente.html' , { 'form' : form } )

def modifica_cliente ( request , pk ):
    cliente = get_object_or_404( Cliente , pk = pk)
    if request.method == 'GET':
        form = FormCliente ( instance = cliente )
        return render ( request , 'form_cliente.html' , { 'form' : form } )
    if request.method == 'POST':
        form = FormImmobili ( request.POST , instance = cliente )
        if form.is_valid() :
            form.save ()
            msg = 'Cliente modificato con successo'
        return render(request, 'rubrica.html', {'msg':msg})

def cancella_cliente ( request , pk ):
    cliente = get_object_or_404( Cliente , pk = pk)
    cliente.delete()
    return redirect( 'gestione_rubrica' )

def aggiungi_immobile ( request ) :
    if request.method == 'POST' :
        form = FormImmobili ( request.POST )
        if form.is_valid () :
            form.save ()
        msg = 'Immobile inserito con successo'
        return redirect('index')
    else :
        form = FormImmobili ()
        formCliente = FormCliente ()
        return render ( request , 'form_immobile.html' , { 'form' : form , 'formCliente' : formCliente } )

@csrf_exempt
def aggiungi_cliente_immobile(request):
    response_data = { }
    if request.method == 'POST':
        cliente = Cliente()
        cliente.nome = request.POST.get ( 'nome' )
        cliente.cognome = request.POST.get ( 'cognome' )
        cliente.citta = request.POST.get ( 'citta' )
        cliente.email = request.POST.get ( 'email' )
        cliente.telefono_fisso = request.POST.get ( 'telefono_fisso' )
        cliente.telefono_cellulare = request.POST.get ( 'telefono_cellulare' )
        cliente.inizio_incarico = request.POST.get ( 'inizio_incarico' )
        cliente.fine_incarico = request.POST.get ( 'fine_incarico' )
        cliente.cliente = request.POST.get ( 'cliente' )
        cliente.scadenza = request.POST.get ( 'scadenza' )
        print(request)
        cliente.save ()

        cliente_pk = Cliente.objects.get(
            nome = request.POST.get ( 'nome' ),
            cognome = request.POST.get ( 'cognome' ),
            citta = request.POST.get ( 'citta' ),
            email = request.POST.get ( 'email' ),
            telefono_fisso = request.POST.get ( 'telefono_fisso' ),
            telefono_cellulare = request.POST.get ( 'telefono_cellulare' ),
            inizio_incarico = request.POST.get ( 'inizio_incarico' ),
            fine_incarico = request.POST.get ( 'fine_incarico' ),
            cliente = request.POST.get ( 'cliente' ),
            scadenza= request.POST.get ( 'scadenza' )
        )
        pk = str(cliente_pk.pk)
        return HttpResponse (pk,content_type="application/json")
    else :
        return HttpResponse (response_data , safe=False, content_type="application/json")


def modifica_immmobile ( request , pk ) :
    immobile_pk = get_object_or_404 ( Immobile , pk=pk )
    if request.method == 'GET' :
        form = FormImmobili ( instance=immobile_pk )
        formCliente = FormCliente ( instance=immobile_pk.cliente )
        return render ( request , 'form_immobile.html' , { 'form' : form , 'formCliente' : formCliente } )
    if request.method == 'POST' :
        form = FormImmobili ( request.POST , instance=immobile_pk )
        if form.is_valid :
            form.save()
            msg = 'Immobile modificato con successo'
            return redirect('index')

def cancella_immobile ( request , pk ):

    immobile = get_object_or_404( Immobile , pk = pk)
    immobile.delete()
    return redirect( 'index' )


class Immobili_vendita(BaseDatatableView):
    model = Immobile
    columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente', 'telefono_cellulare', 'telefono_fisso', 'prezzo',
               'fascia_prezzo', 'tipologia', 'mutuo',
               'immobili_proposti', 'note', 'stato', 'modifica', 'cancella']

    def get_initial_queryset(self):
        return Immobile.objects.filter(cliente__immobile__contratto_id=2).order_by('-id')

    order_columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente', 'telefono_cellulare', 'telefono_fisso', 'prezzo',
                     'fascia_prezzo', 'tipologia', 'mutuo',
                     'immobili_proposti', 'note', 'stato', '', '']

    max_display_length = 10

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(indirizzo__icontains=search) | \
                           Q(citta__icontains=search) | Q(zona__icontains=search) | \
                           Q(cliente__nome__icontains=search) | Q(cliente__cognome__icontains=search) | Q(
                cliente__telefono_cellulare__icontains=search) | \
                           Q(cliente__telefono_fisso__icontains=search) | \
                           Q(prezzo__icontains=search) | Q(fascia_prezzo__fascia_min__icontains=search) | \
                           Q(fascia_prezzo__fascia_max__icontains=search) | Q(tipologia__icontains=search) | \
                           Q(mutuo__icontains=search) | Q(immobili_proposti__icontains=search) | Q(
                note__icontains=search) | Q(stato__icontains=search))
        return qs

    def render_column(self, row, column):
        if column == 'cliente':
            return escape('{0}'.format(row.data))
        if column == 'cliente':
            return escape('{0} {1}'.format(row.cliente.nome, row.cliente.cognome))
        if column == 'telefono_cellulare':
            return escape('{0}'.format(row.cliente.telefono_cellulare))
        if column == 'telefono_fisso':
            return escape('{0}'.format(row.cliente.telefono_fisso))
        if column == 'tipologia':
            return escape('{0}'.format(row.tipologia))
        if column == 'modifica':
            return '<a href="immobili/modifica_immobile/%s"><button type="button" class="btn btn-primary">Modifica</button></a>' % row.pk
        if column == 'cancella':
            return '<a href="immobili/cancella_immobile/%s"><button type="button" class="btn btn-danger">Cancella</button></a>' % row.pk
        else:
            return super(Immobili_vendita, self).render_column(row, column)

class Immobili_affitto(BaseDatatableView):
    model = Immobile
    columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente','telefono_cellulare','telefono_fisso','prezzo','fascia_prezzo','tipologia','mutuo',
               'immobili_proposti', 'note','stato','modifica','cancella']

    def get_initial_queryset(self):
        return Immobile.objects.filter ( cliente__immobile__contratto_id=1 ).order_by('-data')

    order_columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente','telefono_cellulare','telefono_fisso','prezzo','fascia_prezzo','tipologia','mutuo',
                     'immobili_proposti', 'note','stato','','']

    max_display_length = 10

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(indirizzo__icontains=search) | \
                           Q(citta__icontains=search) | Q(zona__icontains=search) | \
                           Q(cliente__nome__icontains=search) | Q(cliente__cognome__icontains=search) | Q(
                cliente__telefono_cellulare__icontains=search) | \
                           Q(cliente__telefono_fisso__icontains=search) | \
                           Q(prezzo__icontains=search) | Q(fascia_prezzo__fascia_min__icontains=search) | \
                           Q(fascia_prezzo__fascia_max__icontains=search) | Q(tipologia__icontains=search) | \
                           Q(mutuo__icontains=search) | Q(immobili_proposti__icontains=search) | Q(
                note__icontains=search) | Q(stato__icontains=search))
        return qs

    def render_column(self, row, column):
        if column == 'cliente':
            return escape('{0} {1}'.format(row.cliente.nome, row.cliente.cognome))
        if column == 'telefono_cellulare':
            return escape('{0}'.format(row.cliente.telefono_cellulare))
        if column == 'telefono_fisso':
            return escape('{0}'.format(row.cliente.telefono_fisso))
        if column == 'tipologia':
            return escape('{0}'.format(row.tipologia))
        if column == 'modifica':
            return '<a href="immobili/modifica_immobile/%s"><button type="button" class="btn btn-primary">Modifica</button></a>' % row.pk
        if column == 'cancella':
            return '<a href="immobili/cancella_immobile/%s"><button type="button" class="btn btn-danger">Cancella</button></a>' % row.pk
        else:
            return super(Immobili_affitto, self).render_column(row, column)

class Immobili_gestione(BaseDatatableView):
    model = Immobile
    columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente','telefono_cellulare','telefono_fisso','prezzo','fascia_prezzo','tipologia','mutuo',
               'immobili_proposti', 'note','stato','modifica','cancella']
    def get_initial_queryset(self):
        return Immobile.objects.filter (cliente__immobile__contratto_id=3)
    order_columns = ['data', 'indirizzo', 'citta', 'zona', 'cliente','telefono_cellulare','telefono_fisso','prezzo','fascia_prezzo','tipologia','mutuo',
                     'immobili_proposti', 'note','stato','','']
    max_display_length = 10

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(indirizzo__icontains=search)|\
                Q(citta__icontains=search)|Q(zona__icontains=search)|\
                Q(cliente__nome__icontains=search)|Q(cliente__cognome__icontains=search)|Q(cliente__telefono_cellulare__icontains=search)|\
                Q(cliente__telefono_fisso__icontains=search)|\
                Q(prezzo__icontains=search)|Q(fascia_prezzo__fascia_min__icontains=search)|\
                Q(fascia_prezzo__fascia_max__icontains=search)|Q(tipologia__icontains=search)|\
                Q(mutuo__icontains=search)|Q(immobili_proposti__icontains=search)|Q(note__icontains=search)|Q(stato__icontains=search))
        return qs

    def render_column(self, row, column):
        if column == 'cliente':
            return escape('{0} {1}'.format(row.cliente.nome, row.cliente.cognome))
        if column == 'telefono_cellulare':
            return escape('{0}'.format(row.cliente.telefono_cellulare))
        if column == 'telefono_fisso':
            return escape('{0}'.format(row.cliente.telefono_fisso))
        if column == 'tipologia':
            return escape('{0}'.format(row.tipologia))
        if column == 'modifica':
            return '<a href="immobili/modifica_immobile/%s"><button type="button" class="btn btn-primary">Modifica</button></a>' % row.pk
        if column == 'cancella':
            return '<a href="immobili/cancella_immobile/%s"><button type="button" class="btn btn-danger">Cancella</button></a>' % row.pk
        else:
            return super(Immobili_gestione, self).render_column(row, column)

class Rubrica(BaseDatatableView):
    model = Immobile
    columns = ['cliente', 'telefono_fisso', 'telefono_cellulare', 'citta', 'indirizzo', 'email', 'iscliente',
               'inizio_incarico', 'fine_incarico', 'scadenza', 'modifica', 'cancella']

    def get_initial_queryset(self):
        return Immobile.objects.all()

    order_columns = ['cliente', 'telefono_fisso', 'telefono_cellulare', 'citta', 'indirizzo', 'email', 'iscliente',
               'inizio_incarico', 'fine_incarico', 'scadenza', '', '']

    max_display_length = 25

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(immobile__indirizzo__icontains=search)|\
                Q(citta__icontains=search)|Q(email__icontains=search)|\
                Q(nome__icontains=search)|Q(cognome__icontains=search)|Q(telefono_cellulare__icontains=search)|\
                Q(telefono_fisso__icontains=search)|\
                Q(inizio_incarico__icontains=search)|Q(fine_incarico__icontains=search)|\
                Q(scadenza__icontains=search)|Q(cliente__icontains=search))
        return qs

    def render_column(self, row, column):
        if column == 'cliente':
            return escape('{0} {1}'.format(row.cliente.nome, row.cliente.cognome))
        if column == 'indirizzo':
            return escape('{0}'.format(row.indirizzo))
        if column == 'telefono_cellulare':
            return escape('{0}'.format(row.cliente.telefono_cellulare))
        if column == 'telefono_fisso':
            return escape('{0}'.format(row.cliente.telefono_fisso))
        if column == 'citta':
            return escape('{0}'.format(row.cliente.citta))
        if column == 'email':
            return escape('{0}'.format(row.cliente.email))
        if column == 'inizio_incarico':
            return escape('{0}'.format(row.cliente.inizio_incarico))
        if column == 'fine_incarico':
            return escape('{0}'.format(row.cliente.fine_incarico))
        if column == 'scadenza':
            return escape('{0}'.format(row.cliente.scadenza))
        if column == 'iscliente':
            return escape('{0}'.format(row.cliente.cliente))
        if column == 'modifica':
            return '<a href="modifica_cliente/%s"><button type="button" class="btn btn-primary">Modifica</button></a>' % row.pk
        if column == 'cancella':
            return '<a href="cancella_cliente/%s"><button type="button" class="btn btn-danger">Cancella</button></a>' % row.pk
        else:
            return super(Rubrica, self).render_column(row, column)
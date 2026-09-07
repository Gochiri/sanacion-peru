"""Genera las páginas italianas a partir de las españolas.

**Un diccionario, no seis archivos duplicados.** Las páginas italianas son las
mismas páginas: misma estructura, mismo CSS, mismos guards. Lo único que cambia
es el texto y a qué custom values apunta. Duplicar los HTML significaría que
cada arreglo hay que hacerlo dos veces y acordarse las dos veces — y no nos
acordaríamos.

Así, además, la traducción queda como **una tabla legible**, que es lo que Luca
puede revisar sin abrir HTML. Es el mismo criterio que `COPY_ES` / `COPY_IT` en
los workflows.

⚠️ **El italiano es PROVISIONAL.** Lo tradujimos nosotros el 6-sep porque el
copy llevaba bloqueado desde el 28-ago esperando a Luca (B4/P-13) y el webinar
italiano es el 26. Lo valida él; cambiar una frase es cambiar una línea de aquí
y volver a correr esto.

    python3 builders/traducir.py

Escribe en `paginas/it/`. Después, para lo que se pega en GHL:

    python3 builders/previsualizar.py --ghl paginas/it/*.html
"""
from __future__ import annotations

import os
import re
import sys

PAGINAS = ["registro", "evento", "gracias", "postulacion", "agenda", "comienza-aqui"]

# La marca italiana es «La Nuova Coscienza» y no «Salud Consciente»: es el
# dominio, es el correo y es con la que Luca ya opera allá (P-11). Poner la
# marca española en una página italiana sería presentarle al público una marca
# que no conoce.
MARCA = "La Nuova Coscienza"

# Frase española → frase italiana. El orden importa: se aplican de la más larga
# a la más corta, para que una frase larga no quede partida por un fragmento
# suyo que también esté en la tabla.
TEXTOS = {
    # ── Comunes a varias páginas ────────────────────────────────────────────
    "Salud Consciente": MARCA,
    "· Nueva Conciencia Formación SAC ·": "· Nueva Conciencia Formación ·",
    "El contenido de esta clase es educativo y de acompañamiento. No constituye diagnóstico ni":
        "Il contenuto di questa lezione è educativo e di accompagnamento. Non costituisce diagnosi né",
    "tratamiento médico, y no sustituye la consulta con un profesional de la salud.":
        "trattamento medico, e non sostituisce il consulto con un professionista della salute.",
    "El acompañamiento de la escuela es educativo. No constituye diagnóstico ni tratamiento":
        "L'accompagnamento della scuola è educativo. Non costituisce diagnosi né trattamento",
    "Este contenido es educativo y de acompañamiento. No constituye diagnóstico ni":
        "Questo contenuto è educativo e di accompagnamento. Non costituisce diagnosi né",
    "médico, y no sustituye la consulta con un profesional de la salud.":
        "medico, e non sostituisce il consulto con un professionista della salute.",

    # ── registro ────────────────────────────────────────────────────────────
    "Clase en vivo · Sin costo": "Lezione dal vivo · Gratuita",
    "Por qué tu cuerpo enfermó, y": "Perché il tuo corpo si è ammalato, e",
    "qué puedes hacer": "cosa puoi fare",
    "para sanarlo.": "per guarirlo.",
    "Una clase en directo donde vas a entender qué está diciendo tu síntoma.":
        "Una lezione dal vivo dove capirai cosa sta dicendo il tuo sintomo.",
    "No se graba ni queda publicada: se ve en vivo, y ya.":
        "Non viene registrata né pubblicata: si vede dal vivo, e basta.",
    "Apartar mi lugar": "Prenota il mio posto",
    "Tomas 40 segundos en registrarte. Te mandamos el acceso por WhatsApp.":
        "Ci metti 40 secondi a iscriverti. Ti mandiamo l'accesso su WhatsApp.",
    "Fecha": "Data",
    "Hora": "Ora",
    "Dónde": "Dove",
    "En línea, en directo": "Online, dal vivo",
    "Costo": "Costo",
    "Sin costo": "Gratuita",
    "A quién le sirve": "A chi serve",
    "Si te reconoces en alguna de estas, esta clase es para ti.":
        "Se ti riconosci in una di queste, questa lezione è per te.",
    "Llevas años con un síntoma que nadie te termina de explicar":
        "Sono anni che convivi con un sintomo che nessuno ti spiega davvero",
    "Te han dado nombres, estudios y tratamientos. Lo que nunca te dieron fue una respuesta al":
        "Ti hanno dato nomi, esami e trattamenti. Quello che non ti hanno mai dato è una risposta al",
    "por qué": "perché",
    "Sospechas que tu cuerpo está respondiendo a algo que viviste":
        "Sospetti che il tuo corpo stia rispondendo a qualcosa che hai vissuto",
    "Notaste que el síntoma apareció después de una pérdida, una ruptura o un susto — y nadie le prestó atención a esa coincidencia.":
        "Hai notato che il sintomo è comparso dopo una perdita, una rottura o uno spavento — e nessuno ha dato peso a quella coincidenza.",
    "Quieres entender antes de decidir qué hacer":
        "Vuoi capire prima di decidere cosa fare",
    "No buscas otra receta. Buscas entender la lógica de lo que te está pasando para poder tomar decisiones con criterio propio.":
        "Non cerchi un'altra ricetta. Cerchi di capire la logica di quello che ti sta succedendo, per poter decidere con criterio tuo.",
    "Lo que casi nadie te dice": "Quello che quasi nessuno ti dice",
    "El síntoma no es el problema. Es el aviso.":
        "Il sintomo non è il problema. È l'avviso.",
    "Durante años te enseñaron a callar lo que el cuerpo dice. Te duele, tomas algo y sigues.":
        "Per anni ti hanno insegnato a zittire quello che il corpo dice. Ti fa male, prendi qualcosa e vai avanti.",
    "Vuelve, tomas otra cosa y sigues. Y cada vez que lo silencias, aprendes un poco más a":
        "Torna, prendi altro e vai avanti. E ogni volta che lo zittisci, impari un po' di più a",
    "desconfiar de la única señal que tu cuerpo tiene para hablarte.":
        "diffidare dell'unico segnale che il tuo corpo ha per parlarti.",
    "El problema de esa lógica no es solo que el síntoma regrese. Es que te acostumbras a vivir":
        "Il problema di questa logica non è solo che il sintomo torna. È che ti abitui a vivere",
    "sin entender tu propio cuerpo, y con el tiempo eso se vuelve miedo: miedo al siguiente":
        "senza capire il tuo corpo, e col tempo questo diventa paura: paura del prossimo",
    "estudio, al siguiente diagnóstico, a lo que venga después.":
        "esame, della prossima diagnosi, di quello che verrà dopo.",
    "En esta clase invertimos el orden. En vez de preguntarnos cómo apagar la señal, nos":
        "In questa lezione invertiamo l'ordine. Invece di chiederci come spegnere il segnale, ci",
    "preguntamos qué está señalando — y qué cambia cuando por fin lo entiendes.":
        "chiediamo cosa sta segnalando — e cosa cambia quando finalmente lo capisci.",
    "En la clase": "Nella lezione",
    "Qué te llevas de esta hora.": "Cosa ti porti via da quest'ora.",
    "La diferencia entre tratar un síntoma y entenderlo, explicada con casos concretos y no con teoría.":
        "La differenza tra trattare un sintomo e capirlo, spiegata con casi concreti e non con la teoria.",
    "Por qué el cuerpo elige un órgano y no otro, y qué tiene que ver eso con lo que estabas viviendo cuando apareció.":
        "Perché il corpo sceglie un organo e non un altro, e cosa c'entra questo con quello che stavi vivendo quando è comparso.",
    "Cómo leer la línea de tiempo de tu propio síntoma para encontrar el momento en que empezó de verdad.":
        "Come leggere la linea del tempo del tuo sintomo per trovare il momento in cui è iniziato davvero.",
    "Qué se puede hacer desde ahí — y qué no —, dicho con honestidad y sin promesas mágicas.":
        "Cosa si può fare da lì — e cosa no —, detto con onestà e senza promesse magiche.",
    "Espacio para preguntas en vivo. Es una clase, no un video pregrabado.":
        "Spazio per domande dal vivo. È una lezione, non un video preregistrato.",
    "Quiénes la dan": "Chi la tiene",
    "Las personas detrás de Salud Consciente.": "Le persone dietro %s." % MARCA,
    "Bioterapeuta": "Bioterapeuta",
    "Registro": "Iscrizione",
    "Aparta tu lugar.": "Prenota il tuo posto.",
    "Son tres preguntas. La última nos dice qué buscas, para mandarte lo que de verdad":
        "Sono tre domande. L'ultima ci dice cosa cerchi, per mandarti quello che ti serve davvero",
    "te sirve y no llenarte de mensajes que no pediste.":
        "e non riempirti di messaggi che non hai chiesto.",
    "Antes de que preguntes": "Prima che tu lo chieda",
    "Lo que más nos consultan.": "Quello che ci chiedono di più.",
    "¿De verdad no tiene costo?": "È davvero gratuita?",
    "No tiene costo. Es una clase en vivo abierta a quien se registre. Al final contamos qué más hacemos, y quien quiera seguir, sigue.":
        "È gratuita. È una lezione dal vivo aperta a chi si iscrive. Alla fine raccontiamo cos'altro facciamo, e chi vuole proseguire, prosegue.",
    "¿Queda grabada?": "Rimane registrata?",
    "No. Se transmite en directo y no queda publicada. Por eso conviene apartar el horario cuando te registres.":
        "No. Va in diretta e non resta pubblicata. Per questo conviene bloccarti l'orario quando ti iscrivi.",
    "¿Esto reemplaza a mi médico?": "Questo sostituisce il mio medico?",
    "No, y no queremos que lo haga. Esto es acompañamiento para entender qué está pasando en tu cuerpo. No sustituye diagnóstico ni tratamiento médico, y no te vamos a pedir que dejes el tuyo.":
        "No, e non vogliamo che lo faccia. Questo è accompagnamento per capire cosa sta succedendo nel tuo corpo. Non sostituisce diagnosi né trattamento medico, e non ti chiederemo di lasciare il tuo.",
    "No sé nada del tema, ¿voy a entender?": "Non so nulla dell'argomento, capirò qualcosa?",
    "Sí. La clase está pensada para quien llega de cero. No hace falta formación previa ni conocer la terminología.":
        "Sì. La lezione è pensata per chi arriva da zero. Non serve formazione precedente né conoscere la terminologia.",
    "¿Cómo me llega el acceso?": "Come mi arriva l'accesso?",
    "Al registrarte te llega por WhatsApp el enlace del grupo, y ahí mandamos el acceso el día de la clase. Revisa que tu número esté bien escrito.":
        "Quando ti iscrivi ti arriva su WhatsApp il link del gruppo, e lì mandiamo l'accesso il giorno della lezione. Controlla che il tuo numero sia scritto bene.",
    "En vivo": "Dal vivo",

    # ── evento ──────────────────────────────────────────────────────────────
    "Preparando la transmisión": "Stiamo preparando la diretta",
    "La clase se abre aquí unos minutos antes de empezar.":
        "La lezione si apre qui qualche minuto prima di iniziare.",
    "Deja esta página abierta.": "Lascia questa pagina aperta.",
    "Después de la clase": "Dopo la lezione",
    "Si quieres llevar esto más lejos, el siguiente paso es postular.":
        "Se vuoi portare tutto questo più lontano, il passo successivo è candidarti.",
    "La escuela no se compra desde aquí. Se postula, hablamos contigo y entre":
        "La scuola non si compra da qui. Ci si candida, parliamo con te e insieme",
    "los dos vemos si tiene sentido que entres. Si no lo tiene, te lo decimos.":
        "vediamo se ha senso che tu entri. Se non ce l'ha, te lo diciamo.",
    "Quiero postular a la escuela": "Voglio candidarmi alla scuola",
    "Son unas preguntas cortas y al terminar eliges el horario de tu llamada.":
        "Sono poche domande e alla fine scegli l'orario della tua chiamata.",
    "Cómo sigue": "Come prosegue",
    "Respondes la postulación": "Rispondi alla candidatura",
    "Nos cuentas qué te pasa y qué buscas. Es lo que nos permite preparar la conversación.":
        "Ci racconti cosa ti succede e cosa cerchi. È quello che ci permette di preparare la conversazione.",
    "Eliges el horario de tu llamada": "Scegli l'orario della tua chiamata",
    "Media hora, por videollamada. Sin costo y sin compromiso de compra.":
        "Un'ora, in videochiamata. Gratuita e senza impegno di acquisto.",
    "Decides con la información completa": "Decidi con tutte le informazioni",
    "Te explicamos el programa, el precio y las formas de pago. Y si no es para ti, te lo decimos ahí mismo.":
        "Ti spieghiamo il programma, il prezzo e le modalità di pagamento. E se non fa per te, te lo diciamo lì.",
    "Esta clase no queda grabada ni publicada.": "Questa lezione non resta registrata né pubblicata.",
    "Esta página está abierta solo": "Questa pagina è aperta solo",
    "durante el ciclo: cuando termina, se cierra. Si te interesó, es mejor postular hoy que":
        "durante il ciclo: quando finisce, si chiude. Se ti ha interessato, meglio candidarsi oggi che",
    "buscarla después.": "cercarla dopo.",

    # ── gracias ─────────────────────────────────────────────────────────────
    "Registro confirmado": "Iscrizione confermata",
    "Tu lugar está apartado.": "Il tuo posto è prenotato.",
    "Ya estás en la lista. Ahora falta una cosa para que no te lo pierdas.":
        "Sei in lista. Ora manca una cosa perché tu non te la perda.",
    "Revisa tu WhatsApp": "Controlla il tuo WhatsApp",
    "Te acabamos de escribir al número que dejaste. Ahí te mandamos el acceso y ahí":
        "Ti abbiamo appena scritto al numero che hai lasciato. Lì ti mandiamo l'accesso e lì",
    "avisamos cuando la clase empieza — es el único sitio donde llega el enlace.":
        "avvisiamo quando la lezione inizia — è l'unico posto dove arriva il link.",
    "Si no ves nada en unos minutos, búscanos en archivados o en spam.":
        "Se non vedi nulla tra qualche minuto, cercaci negli archiviati o nello spam.",
    "De aquí al día de la clase": "Da qui al giorno della lezione",
    "Vas a recibir material estos días": "Riceverai del materiale in questi giorni",
    "Cosas cortas, para ir entrando en tema antes de la clase. Nada que te robe tiempo.":
        "Cose brevi, per entrare in argomento prima della lezione. Niente che ti rubi tempo.",
    "Te recordamos el día antes y un rato antes":
        "Ti ricordiamo il giorno prima e poco prima",
    "Para que no se te pase. La clase no queda grabada, así que el recordatorio importa.":
        "Perché non ti sfugga. La lezione non resta registrata, quindi il promemoria conta.",
    "Entras por el enlace que te llegue a ti": "Entri dal link che arriva a te",
    "Te mandamos uno propio. Es el que usamos para saber que entraste, así que mejor ese que el del grupo.":
        "Te ne mandiamo uno tuo. È quello che usiamo per sapere che sei entrato, quindi meglio quello che quello del gruppo.",

    # ── postulacion ─────────────────────────────────────────────────────────
    "Postulación": "Candidatura",
    "No se compra. Se postula.": "Non si compra. Ci si candida.",
    "La escuela es un proceso largo y no le sirve a todo el mundo. Por eso antes de":
        "La scuola è un percorso lungo e non serve a tutti. Per questo prima di",
    "entrar hay una conversación: para ver juntos si tiene sentido en tu caso.":
        "entrare c'è una conversazione: per vedere insieme se ha senso nel tuo caso.",
    "Respondes estas preguntas": "Rispondi a queste domande",
    "Nos cuentas qué te está pasando y qué te gustaría resolver. Es lo que nos deja preparar la conversación en vez de improvisarla.":
        "Ci racconti cosa ti sta succedendo e cosa vorresti risolvere. È quello che ci lascia preparare la conversazione invece di improvvisarla.",
    "Eliges tu horario en la pantalla siguiente": "Scegli il tuo orario nella schermata successiva",
    "Al enviar te aparece el calendario y escoges cuándo hablamos. Si prefieres pensarlo, también te mandamos el enlace por WhatsApp.":
        "Quando invii ti compare il calendario e scegli quando parliamo. Se preferisci pensarci, ti mandiamo il link anche su WhatsApp.",
    "Hablamos media hora": "Parliamo un'ora",
    "Te explicamos el programa, cuánto cuesta y cómo se paga. Y si vemos que no es tu momento, te lo decimos ahí mismo.":
        "Ti spieghiamo il programma, quanto costa e come si paga. E se vediamo che non è il tuo momento, te lo diciamo lì.",
    "Postular no te compromete a nada. La llamada es sin costo y no hay que decidir":
        "Candidarti non ti impegna a nulla. La chiamata è gratuita e non c'è da decidere",
    "nada durante ella.": "niente durante la chiamata.",
    "Tus datos": "I tuoi dati",
    "Toma 2 minutos": "Ci vogliono 2 minuti",

    # ── agenda ──────────────────────────────────────────────────────────────
    "Postulación recibida": "Candidatura ricevuta",
    "Falta lo último: elegir cuándo hablamos.": "Manca l'ultima cosa: scegliere quando parliamo.",
    "Escoge el horario que mejor te venga. Es una hora por videollamada, con Joaquín.":
        "Scegli l'orario che ti viene meglio. È un'ora in videochiamata, con Luca.",
    "La llamada": "La chiamata",
    "Qué va a pasar ahí.": "Cosa succederà.",
    "Te preguntamos por lo que escribiste, para entender bien tu caso.":
        "Ti chiediamo di quello che hai scritto, per capire bene il tuo caso.",
    "Te contamos cómo funciona la escuela, cuánto dura y qué se espera de ti.":
        "Ti raccontiamo come funziona la scuola, quanto dura e cosa ci si aspetta da te.",
    "Precio y formas de pago, sin rodeos.": "Prezzo e modalità di pagamento, senza giri di parole.",
    "Si vemos que no es tu momento, te lo decimos ahí mismo.":
        "Se vediamo che non è il tuo momento, te lo diciamo lì.",
    "No hay que decidir nada durante la llamada. Y si te surge algo y no puedes,":
        "Non c'è da decidere nulla durante la chiamata. E se ti capita qualcosa e non puoi,",
    "se reprograma desde el mismo correo de confirmación.":
        "si riprogramma dalla stessa email di conferma.",

    # ── comienza-aqui ───────────────────────────────────────────────────────
    "Comienza aquí": "Inizia qui",
    "Por dónde empezar, sin comprometerte con nada.":
        "Da dove iniziare, senza impegnarti in nulla.",
    "Por lo que nos contaste, la escuela no es lo que necesitas ahora mismo —":
        "Da quello che ci hai raccontato, la scuola non è quello che ti serve adesso —",
    "y está bien. Es un proceso largo y exigente, y no todo el mundo llega en":
        "e va bene così. È un percorso lungo ed esigente, e non tutti ci arrivano in",
    "ese momento. Lo que sí tenemos para hoy es esto.":
        "questo momento. Quello che abbiamo per oggi è questo.",
    "El video estará disponible en unos días. Te avisamos por WhatsApp cuando esté.":
        "Il video sarà disponibile tra qualche giorno. Ti avvisiamo su WhatsApp quando c'è.",
    "Son unos minutos. No hace falta saber nada del tema para entenderlo.":
        "Sono pochi minuti. Non serve sapere nulla dell'argomento per capirlo.",
    "Una cosa que conviene decir antes.": "Una cosa che conviene dire prima.",
    "Esto no reemplaza a tu médico, y no queremos que lo haga. Si estás en un":
        "Questo non sostituisce il tuo medico, e non vogliamo che lo faccia. Se stai seguendo un",
    "tratamiento, síguelo. Lo que hacemos aquí va por otro lado: mirar qué estaba":
        "trattamento, continualo. Quello che facciamo qui va da un'altra parte: guardare cosa stava",
    "pasando en tu vida cuando el síntoma apareció, y qué relación puede tener con él.":
        "succedendo nella tua vita quando il sintomo è comparso, e che relazione può avere con lui.",
    "Las dos cosas conviven. De hecho, la gente que mejor le saca provecho a esto suele":
        "Le due cose convivono. Anzi, chi ne trae più beneficio di solito",
    "ser justamente la que está bien acompañada por su médico.":
        "è proprio chi è ben seguito dal proprio medico.",
    "Si quieres seguir": "Se vuoi proseguire",
    "21 Días": "21 Giorni",
    "Es lo más parecido a probar esto por dentro sin meterte en un programa largo.":
        "È la cosa più simile a provare tutto questo da dentro senza entrare in un percorso lungo.",
    "Un ejercicio corto cada día, durante tres semanas.":
        "Un esercizio breve ogni giorno, per tre settimane.",
    "Vas a tu ritmo: cada día se hace en pocos minutos.":
        "Vai al tuo ritmo: ogni giorno si fa in pochi minuti.",
    "Empieza por lo tuyo, no por teoría general.":
        "Parte da quello che è tuo, non dalla teoria generale.",
    "Al terminar sabes si esto te interesa de verdad o no era para ti.":
        "Alla fine sai se questo ti interessa davvero o non faceva per te.",
    "Quiero empezar los 21 Días": "Voglio iniziare i 21 Giorni",
    "Y si más adelante cambia tu momento, la escuela sigue ahí. Te vamos a avisar":
        "E se più avanti cambia il tuo momento, la scuola è sempre lì. Ti avviseremo",
    "cuando abramos la siguiente. Sin insistir.":
        "quando apriremo la prossima. Senza insistere.",

    # ── Atributos que también se leen ───────────────────────────────────────
    "Agenda tu llamada de cierre": "Prenota la tua chiamata",
    "Contenido educativo · %s" % "Salud Consciente": "Contenuto educativo · %s" % MARCA,
    "Formulario de postulacion": "Modulo di candidatura",
    "Formulario de registro": "Modulo di iscrizione",
}

# ☠️ Los ids de formulario van escritos en el HTML, no en un custom value, así
# que la tabla de textos no los toca. Sin esto, la página italiana embebe la
# encuesta española: el visitante lee italiano y rellena un formulario en
# español que además lo marca como Perú-LATAM y lo mete en WF2, no en WF2-IT.
FORMULARIOS = [
    ("iheVfI7xkesInu8jKLKB", "UTqIwgAEt0xjmcBeA75j"),   # F01 registro   → F02
    ("DTwkB4aTiEIqUGNI9Qjo", "bGZjMxYQ78jACMs2keUO"),   # F03 postulación → F03-IT
]

# Los custom values se cambian por regla, no a mano.
VALORES = [
    (r"custom_values\.link_calendario_cierre_pe", "custom_values.link_calendario_cierre_it"),
    (r"custom_values\.hora_evento_pe", "custom_values.hora_evento_it"),
    (r"custom_values\.logo_url\b", "custom_values.logo_url_it"),
    (r"custom_values\.([a-z_]+)_es\b", r"custom_values.\1_it"),
]

# Rastros de que una frase se escapó de la tabla. Se buscan en lo generado.
RASTROS = ["ñ", "¿", "¡", " qué ", " está ", " aquí ", " cómo ", " tú ", "ción ",
           " para ti", " puedes ", " tienes ", "Cuándo", " año", " síntoma"]

# Nombres propios que son español y se quedan así: la razón social es la que
# figura en el registro peruano, y traducirla sería inventarse una empresa.
NO_SE_TRADUCE = ["Nueva Conciencia Formación", "Christie Salvatierra",
                 "Luca Stefanizzi", "Joaquín"]


def traducir(html: str) -> str:
    # De la más larga a la más corta: si no, una frase corta que sea trozo de
    # otra larga la parte por dentro y la larga ya no encuentra su original.
    for es in sorted(TEXTOS, key=len, reverse=True):
        html = html.replace(es, TEXTOS[es])
    for patron, reemplazo in VALORES:
        html = re.sub(patron, reemplazo, html)
    for es, it in FORMULARIOS:
        html = html.replace(es, it)
    return html


def limpio(html: str) -> list[str]:
    """Lo que queda en español después de traducir, mirando solo el texto visible."""
    s = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    visible = " ".join(x.strip() for x in re.split(r"<[^>]+>", s) if x.strip())
    for propio in NO_SE_TRADUCE:
        visible = visible.replace(propio, "")
    return sorted({r.strip() for r in RASTROS if r in visible})


def main() -> None:
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, "paginas", "it")
    os.makedirs(destino, exist_ok=True)

    # Un id español que sobreviva es un fallo silencioso: la página se ve
    # italiana y el formulario rutea al mercado equivocado.
    espanoles = [es for es, _ in FORMULARIOS]

    fallos = 0
    for nombre in PAGINAS:
        origen = os.path.join(raiz, "paginas", "%s-es.html" % nombre)
        html = traducir(open(origen).read())

        cabecera = (
            "<!--\n"
            "  %s · versión italiana\n"
            "  GENERADO por builders/traducir.py — no editar aquí.\n"
            "  El texto se cambia en la tabla TEXTOS de ese script y se vuelve a generar.\n"
            "  Traducción PROVISIONAL del 6-sep: la valida Luca (B4/P-13).\n"
            "-->\n" % nombre
        )
        salida = os.path.join(destino, "%s-it.html" % nombre)
        open(salida, "w").write(cabecera + html)

        sobra = limpio(html)
        formularios = [e for e in espanoles if e in html]
        aviso = ""
        if sobra:
            aviso += "  ✗ ESPAÑOL: %s" % sobra
        if formularios:
            aviso += "  ✗ FORMULARIO ESPAÑOL: %s" % formularios
        print("%-16s → paginas/it/%s-it.html%s" % (nombre, nombre, aviso))
        fallos += bool(sobra or formularios)

    print()
    if fallos:
        raise SystemExit("%d página(s) con español sin traducir." % fallos)
    print("Las seis, sin rastros de español.")
    print("Para lo que se pega en GHL:")
    print("  python3 builders/previsualizar.py --ghl paginas/it/*.html")


if __name__ == "__main__":
    main()

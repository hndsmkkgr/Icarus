define i = Character("Icarus")
define d = Character("Daedalus", color = "#C2DF97")
define r = Character("Rigel", color = "#67C8FF")
define l = Character("Luna", color = "#FF6FAE")
define b = Character("Belphegor", color = "#99D94D")
define m = Character("Minos", color = "#FF3052")
define bg = Character("Bodyguard", color = "#CCC8C5")
define om = Character("Old man", color = "#CCC8C5")
define ow = Character("Old woman", color = "#CCC8C5")
define g = Character("Girl", color = "#CCC8C5")
define bo = Character("Boy", color = "#CCC8C5")
define p = Character("Man", color = "#CCC8C5")
define w = Character("Woman", color = "#CCC8C5")
define s = Character("Scientist", color = "#CCC8C5")

image icarusN flip = im.Flip("icarus neutral.png", horizontal=True)
image lunaN flip = im.Flip("luna neutral.png", horizontal=True)
image rigelN flip = im.Flip("rigel neutral.png", horizontal=True)
image minosN flip = im.Flip("minos neutral.png", horizontal=True)
image belphegorN flip = im.Flip("belphegor neutral.png", horizontal=True)

image lunaT flip = im.Flip("luna think.png", horizontal=True)
image lunaSad flip = im.Flip("luna sad.png", horizontal=True)
image lunaAng flip = im.Flip("luna angry.png", horizontal=True)
image lunaSigh flip = im.Flip("luna sigh.png", horizontal=True)
image lunaPout flip = im.Flip("luna pout.png", horizontal=True)
image lunaLaugh flip = im.Flip("luna laugh.png", horizontal=True)
image lunaSurp flip = im.Flip("luna surprised.png", horizontal=True)
image rigelSD flip = im.Flip("rigel sweatdrop.png", horizontal=True)
image rigelSigh flip = im.Flip("rigel sigh.png", horizontal=True)
image rigelAng flip = im.Flip("rigel angry.png", horizontal=True)
image rigelLaugh flip = im.Flip("rigel laugh.png", horizontal=True)
image icarusDet flip = im.Flip("icarus determined.png", horizontal=True)
image icarusSurp flip = im.Flip("icarus surprised.png", horizontal=True)
image icarusLaugh flip = im.Flip("icarus laugh.png", horizontal=True)

image journal1 = "gui/journal1.png"
image journal2 = "gui/journal2.png"
image journal3_1 = "gui/journal3_1.png"
image scanner = "gui/scanner.png"
image draftingTube = "gui/draftingTube.png"
image noteLuna1 = "gui/noteLuna1.png"
image noteLuna2 = "gui/noteLuna2.png"
image solarcell = "gui/solarcell.png"
image antena = "gui/antena.png"
image laser = "gui/laser.png"

init python:
    currentsun = 0
    maxsun = 300
    currentrep = 0
    maxrep = 150

init -1 python:
    import renpy.store as store
    import renpy.exports as renpy # we need this so Ren'Py properly handles rollback with classes
    from operator import attrgetter # we need this for sorting items

    inv_page = 0 # initial page of teh inventory screen
    item = None
    class Player(renpy.store.object):
        def __init__(self, name, element=None):
            self.name=name
            self.element=element

    class Item(store.object):
        def __init__(self, name, player=None, element="", image=""):
            self.name = name
            self.player=player # which character can use this item?
            self.image=image # image file to use for this item
        def use(self): #here we define what should happen when we use the item
                player.element=self.element #item to change elemental damage; we don't drop it, since it's not a consumable item

    class Inventory(store.object):
        def __init__(self):
            # self.money = money
            self.items = []
        def add(self, item): # a simple method that adds an item; we could also add conditions here (like check if there is space in the inventory)
            self.items.append(item)
        def drop(self, item):
            self.items.remove(item)

    def item_use():
        item.use()

    #Tooltips:
    style.tips_top = Style(style.default)
    # style.tips_top.size=12
    style.tips_top.color="ffffff"
    style.tips_top.outlines=[(1, "ffffff", 0,0)]
    style.tips_top.kerning = 5

    style.tips_bottom = Style(style.tips_top)
    style.tips_top.size=14
    style.tips_bottom.outlines=[(0, "ffffff", 0, 0)]
    style.tips_bottom.kerning = 2

    style.button.background=Frame("gui/frames.png", 25, 25)
    style.button.yminimum=52
    style.button.xminimum=52
    style.button_text.color="FFFFFF"


    showitems = True #turn True to debug the inventory

screen inventory_button():
    textbutton "Show Inventory" action [ Show("inventory_screen"), Hide("inventory_button")] align (.95,.005)

screen inventory_screen():
    add "gui/inventory.png" # the background
    modal True #prevent clicking on other stuff when inventory is shown
    hbox align (.95,.0) spacing 20:
        textbutton "Close Inventory" action [ Hide("inventory_screen"), Show("inventory_button"), Return(None)]
    $ x = 515 # coordinates of the top left item position
    $ y = 25
    $ i = 0
    $ sorted_items = sorted(inventory.items, reverse=True) # we sort the items, so non-consumable items that change elemental damage (guns) are listed first
    $ next_inv_page = inv_page + 1
    if next_inv_page > int(len(inventory.items)/9):
        $ next_inv_page = 0
    for item in sorted_items:
        if i+1 <= (inv_page+1)*9 and i+1>inv_page*9:
            $ x += 190
            if i%3==0:
                $ y += 170
                $ x = 515
            $ pic = item.image
            $ my_tooltip = "tooltip_inventory_" + pic.replace("gui/", "").replace(".png", "") # we use tooltips to describe what the item does.
            imagebutton idle pic hover pic xpos x ypos y action [Hide("gui_tooltip"), Show("inventory_button"), SetVariable("item", item)] hovered [Show("gui_tooltip", my_picture=my_tooltip, my_tt_ypos=627) ] unhovered [Hide("gui_tooltip")] at inv_eff
            if player.element and (player.element==item.element): #indicate the selected item
                add "gui/selected.png" xpos x ypos y anchor(.5,.5)
        $ i += 1
        if len(inventory.items)>9:
            textbutton _("Next Page") action [SetVariable('inv_page', next_inv_page), Show("inventory_screen")] xpos .475 ypos .83

screen gui_tooltip (my_picture="", my_tt_xpos=58, my_tt_ypos=687):
    add my_picture xpos my_tt_xpos ypos my_tt_ypos

init -1:
    transform inv_eff: # too lazy to make another version of each item, we just use ATL to make hovered items super bright
        zoom 0.5 xanchor 0.5 yanchor 0.5
        on idle:
            linear 0.2 alpha 1.0
        on hover:
            linear 0.2 alpha 2.5

    image information = Text("INFORMATION", style="tips_top")
    #Tooltips-inventory:

    image tooltip_inventory_journal1=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("2113 September (7 tahun lalu) - Hari ini aku berhasil menemukan sebuah konsep untuk membuat solar power satellite. Konsep ini digagas oleh Peter Glaser. Aku akan mencoba mengembangkannya. Ini akan sangat bermanfaat untuk Ílios.(-D)", style="tips_bottom"))
    image tooltip_inventory_journal2=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("2114 Maret (6 tahun lalu) - Aku sudah mulai mengembangkan konsep SPS itu. Tapi masih saja ada kesalahan yang belum terpecahkan. Aku akan mencobanya lagi. (-D)", style="tips_bottom"))
    image tooltip_inventory_journal3_1=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("2112 Juli (8 tahun lalu) - Aku merasa  masalah teknologi yang sekarang digunakan bangsa ini masih kurang memuaskan. Menurutku pasti ada cara agar Ilios mampu mendapatkan energi meski pada malam hari", style="tips_bottom"))
    image tooltip_inventory_journal3_2=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Setelah meneliti sekian lama, akhirnya ku menemukan solusi, tetapi diriku kekurangan banyak komponen. Sekian banyak buku kuno telah kubaca dan siapa sangka teknologi dari sekian abad lalu begitu menarik walau belum sempurna, akan ku sempurnakan", style="tips_bottom"))
    image tooltip_inventory_journal3_3=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Ku rasa alat photovoltaic dari panel surya bisa dipakai untuk alat ini. Kemungkinan penemuan ini bisa kugunakan untuk membuat solar power satellite agar Ílios tetap mendapatkan energi surya dalam kondisi apapun. Projek ini kusebut: SPS.11. (-D)", style="tips_bottom"))
    image tooltip_inventory_noteLuna1=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Kode dari laptop Daedalus:\n115 111 108 97 114 99 101 108 108", style="tips_bottom"))
    image tooltip_inventory_noteLuna2=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Komponen:\nSolar cell, Laser, Antenna", style="tips_bottom"))
    image tooltip_inventory_noteLuna3=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("a = 97, A = 65, z = 122, Z = 90", style="tips_bottom"))
    image tooltip_inventory_solarcell=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Solar Cell adalah suatu perangkat atau komponen yang dapat mengubah energi cahaya matahari menjadi energi listrik\nKomponen ini akan digunakan untuk membangun teknologi yang diteliti Daedalus", style="tips_bottom"))
    image tooltip_inventory_antena=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Antenna, salah satu komponen yang dibutuhkan untuk merakit teknologi yang sedang diteliti Daedalus", style="tips_bottom"))
    image tooltip_inventory_laser=LiveComposite((665, 73), (3,0), ImageReference("information"), (3,30), Text("Laser, salah satu komponen yang dibutuhkan untuk merakit teknologi yang sedang diteliti Daedalus", style="tips_bottom"))

screen sunbar():
    text "Sun Power: [currentsun]" xalign 0.0 yalign 0.0
    bar value currentsun range maxsun xalign 0.0 yalign 0.05 xmaximum 300

screen repbar():
    text "Reputation: [currentrep]" xalign 0.0 yalign 0.0
    bar value currentrep range maxrep xalign 0.0 yalign 0.05 xmaximum 150


init:

    python:

        import math

        class Shaker(object):

            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }

            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child

            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor

                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)

        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)

            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)


################################################################################
# The game starts here.

label start:
    python:
        noteLuna1 = Item("Catatan Luna 1", image="gui/noteLuna1.png")
        noteLuna2 = Item("Catatan Luna 2", image="gui/noteLuna2.png")
        noteLuna3 = Item("Catatan Luna 3", image="gui/noteLuna3.png")
        solarcell = Item("Solar Cell", image="gui/solarcell.png")
        antena = Item("Antenna", image="gui/antena.png")
        laser = Item("Antenna", image="gui/laser.png")
        Journal1 = Item("Journal 1", image="gui/journal1.png")
        Journal2 = Item("Journal 2", image="gui/journal2.png")
        Journal3_1 = Item("Journal 3 page 1", image="gui/journal3_1.png")
        Journal3_2 = Item("Journal 3 page 2", image="gui/journal3_2.png")
        Journal3_3 = Item("Journal 3 page 3", image="gui/journal3_3.png")

        player = Player("Icarus")
    init python:
        inventory = Inventory()

    play music "music/Ever Mindful.mp3" loop

    scene bg testbg
    "..."
    "Oh, halo..."
    "Siapakah engkau?"
    "Apakah kau tersesat?"
    "Kau sedang berada di Ílios, negeri matahari"
    "Negeri yang berjaya dengan kekayaan yang melimpah"
    "Negeri ini sangatlah berjaya hingga suatu ketika segalanya runtuh"
    "Jutaan jiwa bangsa Ílios menangis, merintih kesakitan, mereka kehilangan segalanya"
    "Seluruh negeri menjadi gelap gulita."
    "Tidak ada harapan sepanjang mata memandang"
    "Hingga..."
    "Hingga suatu cahaya turun, seorang penyelamat, sang pembawa cahaya--"
    "atau seorang penghancur, sang pembawa kegelapan yang akan menyelimuti Ílios dalam kegelapan selamanya"
    "Ah..."
    "Ku baru ingat..."
    "Cahaya yang turun itu adalah engkau"
    "Maka buatlah keputusan yang tepat"
    "Hanya engkau yang dapat menyelamatkan negeri ini"

    image black = "#000"
    scene black with dissolve
    show icarus neutral

    i "Halo"
    i "Aku Icarus, marilah bantu aku menyelamatkan negeri ini"
    i "Aku akan memberi sedikit arahan bagi kalian"
    #
    # python:
    #     name = renpy.input("My name is: ")
    #     name = name.strip()
    #

    # i "Nice to meet you, [name].\nI hope you'll enjoy the game!"

    show screen sunbar

    i "Lihatkah bar di sebelah kiri atas itu?"
    i "Bar itu disebut dengan SUN POINTS BAR. Poin pada bar tersebut dapat bertambah ataupun berkurang seiring kalian menemukan teknologi yang dapat digunakan untuk memperoleh energi surya"

    hide screen sunbar
    show screen repbar with dissolve

    i "Selanjutnya adalah REPUTATION BAR, poin pada bar tersebut dapat bertambah ataupun berkurang seiring kalian membuat keputusan"
    i "Game ini memiliki banyak percabangan, dan pada saat itu kalian akan dituntut untuk membuat keputusuan, apakah kalian akan berbuat aksi A, aksi B, atau aksi lainnya"
    i "Ku akan memberi kalian 50 REPUTATION POINTS hanya sebagai ilustrasi"
    $ currentrep +=50
    i "Lalu berikut contoh tampilan opsi"

    default x = False
    menu:
        "Opsi yang benar":
            $ x = True
            $ currentrep +=50
            jump opt
        "Opsi yang salah":
            $ currentrep -=50
            jump opt

    label opt:
        $ renpy.fix_rollback()
        if x:
            i "Kalian memilih tindakan yang benar!"
            i "Lihat, kalian mendapatkan 50 REPUTATION POINTS"
            i "Hebat"
        else:
            i "Aww sayang sekali, REPUTATION POINTS kalian berkurang 50"
            i "Tetapi jangan khawatir, ini hanyalah contoh"

    hide screen sunbar
    hide screen repbar
    $ currentrep = 0

    i "Yang perlu kalian perhatikan adalah, sekalinya kalian memilih suatu opsi, kalian tidak dapat kembali dan memilih opsi lain"
    i "Maka dari itu pikirkanlah dan pertimbangkanlah pilihan kalian dengan baik-baik"

    i "Baik selanjutnya adalah INVENTORY"
    show screen inventory_button
    i "Lihatlah di pojok kanan atas, jika diklik maka akan ditampilkan item-item yang kalian dapatkan selama bermain"
    i "Hm.... sepertinya cukup sampai di sini saja tutorialnya, aku yakin kalian pasti bisa membantuku"
    i "Sampai jumpa, kawan!"
    hide screen inventory_button

    scene black with dissolve
    scene bg ilios with dissolve

    "Ílios adalah bangsa yang besar, makmur, dan kaya akan sumber daya alam."
    "Mereka memiliki tambang emas yang sangat besar, hampir seluruh rakyatnya tinggal dalam kemewahan."
    "Dahulu kala bangsa ini sangatlah kaya raya akan bahan bakar fosil seperti minyak bumi dan batu bara."
    "Tetapi karena keserakahan bangsa tersebut, seluruh bahan bakar fosil itu terkuras dan sangat sulit untuk ditemukan lagi. Bangsa Ílios sempat mengalami krisis energi dan rakyat-rakyatnya menderita"
    "Hingga sang raja pun akhirnya bertindak dan membuat perubahan yang sangat besar. Perubahan tersebut tidak akan pernah dilupakan bangsa Ílios."
    "Perlahan bangsa ini mengganti kebergantungan terhadap sumber energi yang tak terbarukan ke energi terbarukan, yaitu matahari"
    "Tenaga surya adalah energi dari matahari yang diubah menjadi energi panas atau listrik. Energi matahari adalah sumber energi terbarukan yang paling bersih dan paling berlimpah yang tersedia, dan AS memiliki beberapa sumber daya surya terkaya di dunia."
    "Teknologi surya dapat memanfaatkan energi ini untuk berbagai keperluan, termasuk menghasilkan listrik, menyediakan cahaya atau lingkungan interior yang nyaman, dan memanaskan air untuk keperluan rumah tangga, komersial, atau industri.\n~Solar Energy Industries Association"

    "Negeri ini memperoleh energi matahari di siang hari dan menyimpannya pada baterai besar sehingga pada malam hari pun negeri ini tetap penuh kehidupan"

    scene bg ignisawal
    "Negeri matahari ini dikelilingi gurun pasir yang sangatlah luas, dan pada gurun tersebut terdapat gunung yang besar dan gagah setinggi 2500m."
    "Gunung tersebut dikenal dengan nama Ignis"
    "Ada sebuah legenda bahwa ratusan tahun yang lalu gunung Ignis meletus dan menyebabkan setengah dari belahan dunia merasakan dampak yang sangat luar biasa"

    scene bg townhall
    "22 Oktober 2120"
    "Hari Kebangkitan Ílios yang ke-50"
    "Masyarakat berkumpul di townhall merayakannya"
    "Tak terkecuali Raja Minos sang pemimpin Bangsa Ílios"

    scene bg hidupminos
    play sound "sounds/crowd.mp3" loop

    "Raja Minos adalah raja yang baik hati, apapun akan dilakukan demi kenyamanan dan keselamatan rakyatnya"
    m "Ini adalah hari yang sangat besar bagi bangsa kita"
    m "tepat di hari ini, 50 tahun yang lalu, Raja Meon, raja yang memimpin jauh sebelum saya telah memberi harapan dan membangkitkan kejayaan bangsa ini"
    m "Rakyat-rakyatku mari kita ramaikan perayaan ini"
    p "HIDUP RAJA MINOS"
    w "Ílios FOREVER"
    ow "Raja Minos selalu membawa keadilan"
    om "benar!"

    stop sound

    scene bg perumahan with dissolve

    "Di Ílios ada seorang peneliti yang sangat terkenal akan karyanya, ia telah memajukan teknologi energi matahari lebih dari apa yang dapat dibayangkan siapa pun"
    "Sang raja dan seluruh masyarakat Ílios sangatlah berterimakasih padanya"
    show daedalus neutral with dissolve
    "Peneliti tersebut bernama Daedalus, dia merupakan orang yang sangat jenius dan sayang dengan keluarganya"
    hide daedalus neutral with dissolve
    show icarus neutral with dissolve
    "Dia tinggal bersama anak semata wayangnya yang bernama Icarus"
    "Bisa dibilang Icarus mirip dengan Daedalus, dia sangat ingin tahu dengan banyak hal"
    "Namun disamping itu dia sangat keras kepala"
    hide icarus neutral with dissolve
    show icarusN flip at left with dissolve
    show daedalus neutral at right with dissolve
    "Sejak kecil dia tinggal dengan ayahnya"
    "Ibu Icarus meninggal saat melahirkan Icarus"
    "Daedalus yang kehilangan istrinya dapat melihat kembali harapan dari anaknya, ia membesarkannya dengan penuh kasih sayang."
    "Maka dari itu Icarus sangat dekat dengan ayahnya. Mereka bersikap layaknya sahabat, Daedalus sering menceritakan soal penelitian-penelitiannya, betapa indahnya ilmu pengetahuan itu, mereka selalu berbagi cerita dan bersenda gurau,"
    hide icarusN flip at left with dissolve
    hide daedalus neutral at right with dissolve

    scene bg daedanica with dissolve

    i "Guten Morgen, daddy!"
    d "Ohh, selamat pagi, Icarus. Sejak kapan kamu berbahasa Jerman nak hahaha"
    i "Sejak pagi ini haha.\nPah, cappucinonya sudah kutaruh di meja ya "
    d "Oh terimakasih..."
    d "Nak, cappuccino buatanmu, numero uno"
    i "Ya iya lah"
    d "..."
    d "Aku tarik kembali ucapanku tadi"
    i "PAPA!"
    d "Hahaha, iya iya... Cappucino buatanmu memang selalu enak."
    d "Nak, aku sebentar lagi aku akan berangkat kerja, kemungkinan tidak akan pulang hingga besok sore. Kamu jangan hancurin rumah dan jangan kelayapan"
    i "Lahh, kok kerja bukan kah hari ini libur karena perayaan kebangkitan Ílios?"
    d "Ya hari ini libur... tapi aku harus tetap ke lab"
    i "Ayolah pah! Beristirahat sehari saja.. ayo ke townhall bersama aku"
    d "Jangan seperti anak kecil Icarus.. pergilah dengan teman-temanmu"
    d "Ada PENELITIAN penting yang harus ku selesaikan"
    i "huffft... baiklahh"

    scene bg goodbye with dissolve

    d "Aku berangkat dulu ya, nak"
    i "Papa tidak mau sarapan dulu? Nanti sakit lho, udah tua kan makin rentan sakit-sakitan"
    d "Heh sembarangan, aku ini masih muda! Nanti papa sarapan di kantin tempat kerja saja"
    i "Baiklah, kalau begitu kerja yang bener ya pah, jangan main-main nuklir doang"
    d "Sembarangan aja ngomongnya! Papa ga kasih oleh-oleh nanti hahaha"
    d "Papa pergi dulu, jaga diri baik-baik, jangan sampai diculik pas lagi perayaan"
    i "Hey aku ini sudah dewasa ya!"
    d "Hahaha... Dadah Icarus"
    i "Dadah papa"

    "Daedalus pun pergi bekerja."

    scene bg perumahan with dissolve
    "Sementara itu, di luar rumah ada dua orang yang nampaknya telah menunggu-nunggu Icarus"

    show rigel neutral at right
    r "WOY! Icarus dari tadi ditungguin juga ayo cepetan! Kita telat ini, kudengar Raja Minos sudah hampir selesai memberi kata sambutan."

    "Rigel adalah salah sahabat Icarus, dia adalah orang yang labil dan mudah sakit hati , namun pemberani dan pantang menyerah."

    show lunaN flip at left
    l "Iya Icarus, ayo cepat, supaya antrian makanan di food stallnya belum terlalu panjang"

    "Luna juga merupakan sahabat Icarus, dia adalah orang yang teliti, berwawasan luas, dan cinta lingkungan, tetapi ia cukup cerewet."

    show icarus neutral
    i "Iya iya, aku jalan nih!"
    r "Hey, btw... Nanti mau nyoba jajanan apa dulu?"
    l "Hmmm terserah sih, aku ngikut kalian saja"
    i "Bagaimana kalau..."

    default verb = ""
    default prod = ""
    default stand = ""
    menu:
        "Soy Matcha di stand Janji Batin":
            $ verb = "minum"
            $ prod = "Soy Matcha"
            $ stand = "Janji Batin"
            jump opt2
        "Crepe Coklat di stand Achelio Crepes":
            $ verb = "makan"
            $ prod = "Crepe Coklat"
            $ stand = "Achelio Crepes"
            jump opt2
        "Burger Bleber di standnya Kakek Theo":
            $ verb = "makan"
            $ prod = "Burger Bleber"
            $ stand = "Kakek Theo"
            jump opt2
    label opt2:
        $ renpy.fix_rollback()
        hide lunaN flip
        show lunaT flip at left
        l "Hmmm... Tidak ah, ku lagi ga mood [verb] [prod]"
        hide rigel neutral
        show rigel sweatdrop at right
        r "Lah tadi katanya terserah"
        hide lunaT flip
        show lunaSigh flip at left
        l "Iya, terserah tapi jangan [prod]"
        hide rigel sweatdrop
        show rigel sigh at right
        r "Luna oh Luna... Terserah tapi ga mau ini ga mau itu"

    hide lunaSigh flip
    hide rigel sigh
    i "..."
    i "Oh... Guys, sebentar... Sepertinya tabletku tertinggal, nanti aku tidak bisa membeli apa-apa, semua saldoku di situ"
    hide icarus neutral
    show rigel sigh at right
    r "AH kau ini, ada-ada aja. Kamu ini udah kayak kakek-kakek pikun"
    show lunaN flip at left
    l "Yasudah cepatlah ambil tabletmu"
    hide rigel sigh
    hide lunaN flip

    show icarus neutral
    i "Aku balik dulu ke rumah, kalian duluan aja. Nanti kususul!"
    show rigel annoyed at right
    r "Oke, cepat ya. Aku ga mau sampai kita antri kepanjangan apalagi kehabisan jajanan pas sampai di sana"
    show lunaN flip at left
    l "Kami tunggu di townhall ya, Icarus"
    i "Iya!"

    scene bg townhall with dissolve
    play sound "sounds/crowd.mp3"
    show rigel annoyed at right with dissolve
    r "ARGHHH SIAL! Sudah ramai, kalau begini mah fix kita antri panjang buat jajan"
    show lunaN flip at left with dissolve
    l "Yasudahlah Rigel, paling tidak kita tidak telat untuk melihat Raja Minos"

    scene bg hidupminos with dissolve
    show rigel annoyed at right with dissolve
    r "Ini semua karena kita nungguin Icarus, kalau tidak aku pasti sudah [verb] [prod]"
    r "Lihat saja nanti pas anak itu datang, ku ketekin dia sampe mampus!"

    scene bg livingroom with dissolve
    "Seraya Rigel dan Luna merayakan hari kebangkitan Ílios, Icarus sibuk mencari-cari tabletnya yang tertinggal."
    show icarus neutral
    i "Huft...."
    i "Oke... Di manakah aku terakhir menaruh tabletku"

    label menuCariTab:
        scene bg perumahan
        show icarus neutral
        menu:
            "Cek dapur":
                i "Mungkin ada di dapur"
                scene bg dapur
                jump opt3
            "Cek kamar":
                scene bg kamarica
                i "Hmmm... Nampaknya tidak ada di kamar"
                jump menuCariTab
            "Cek ruang tengah":
                scene bg livingroom
                i "Hmmm... Nampaknya tidak ada di ruang tengah"
                jump menuCariTab

    label opt3:
        i "Hmmm..."
        i "Ah! ini dia ketemu!"
        scene bg tab1
        pause
        scene bg tab2
        play sound "sounds/beep.mp3"
        i "Sial, lowbat! Ku harus bawa solar charger kalau begitu"
        i "Semoga aku tidak terlalu telat, bisa-bisa Rigel marah"

    play sound "sounds/rumble.mp3"
    pause
    hide icarus neutral
    show icarus surprised
    i "Hah? Suara apa itu barusan"
    stop sound
    i "Apa tadi cuma perasaanku saja?"

    play sound "sounds/rumble.mp3"
    scene bg hidupminos with dissolve and Shake((0, 0, 0, 0), 3.0, dist=30)
    pause
    show luna surprised at right
    l "Woah!"
    stop sound
    l "Hey! Rigel Kamu ngerasain getaran kah barusan?"
    show rigelSigh flip at left
    r "Hah? Nggak, perasaanmu aja kali, ini kan lagi rame, palingan tadi kamu cuma terdorong dikit"
    hide luna surprised
    show luna think at right
    l "Uhh... Iya juga ya"

    scene bg livingroom with dissolve
    show icarus determined with dissolve
    i "Sip, ku udah mengecek semuanya, tidak ada yang tertinggal lagi"
    play sound "sounds/rumble.mp3"
    scene bg livingroom with Shake((0, 0, 0, 0), 3.0, dist=30)
    show icarus surprised with dissolve
    i "AH! Ini getaran yang tadi kurasakan!"
    stop music

    scene bg ilios
    "Tidak ada yang tahu bahwa hari penuh senyum dan tawa itu akan menjadi hari yang penuh isak tangis dan penderitaan."
    "Gunung Ignis yang ratusan tahun tertidur terbangun pada saat itu, seakan-akan mengamuk pada seluruh umat manusia"
    play music "music/Burnt Spirit.mp3" loop fadein 1.0

    play sound "sounds/rumble.mp3"
    scene bg ignisawal with Shake((0, 0, 0, 0), 3.0, dist=30)
    play sound "sounds/explosion.mp3"
    scene bg ignismeletus with Shake((0, 0, 0, 0), 3.0, dist=30)

    play sound "sounds/scream.mp3"
    scene bg gedebagbug with Shake((0, 0, 0, 0), 3.0, dist=30)
    pause
    stop sound
    scene bg ilios2
    pause

    play sound "sounds/fire.mp3"
    image gifbakar = Movie(size=(1280, 720), xpos=0, ypos=0, xanchor=0, yanchor=0)
    play movie "gifbakar.ogv" loop
    hide movie with dissolve
    stop movie
    play movie "gifbakar.ogv" loop
    hide movie with dissolve
    stop movie

    scene bg iliosbakar with dissolve
    pause
    stop sound

    scene black with dissolve
    pause

    scene bg perumahan2
    "Icarus yang beruntung karena berlindung di ruang darurat dalam rumahnya yang cukup jauh dari gunung tersebut selamat dari bencana itu"
    "Ya meski rumahnya porak poranda, banyak barang rusak karena terjatuh dan dinding yang retak, setidaknya nyawanya tidak hilang"
    "Setelah getaran itu mereda, Icarus pun keluar untuk melihat keadaan"
    show icarus surprised
    i "ASTAGA, APA YANG TERJADI?!"

    scene bg iliosbakar
    play sound "sounds/scream.mp3"
    "Teriakkan terdengar dari setiap sudut kota, orang-orang berlarian di sana-sini, terlihat dari kejauhan banyak bangunan di ujung barat kota terbakar, dan udara dipenuhi abu gelap"
    "Bahkan sudah terlihat beberapa tubuh tak bernyawa tergeletak di beberapa sudut jalanan, mati terinjak-injak warga yang berusaha menyelamatkan diri"
    "Ílios runtuh"
    "Bangsa yang berjaya itu kini porak poranda"
    "Icarus pun mencoba menelpon ayahnya"
    stop sound
    show icarus worried
    i "Ayolah pah... Angkatlah teleponku... Kumohon"
    "Tetapi dikarenakan gangguan sinyal yang parah, Icarus tidak dapat menghubungi ayahnya"
    i "Astaga, apa yang harus kulakukan"


    default telpR = True
    default telpL = True
    default telpD = True
    label telepon:
        $ renpy.fix_rollback()
        if telpR == False and telpL == False and telpD == False:
            jump doneTelepon
        menu:
            "Telepon Rigel" if telpR == True:
                $ renpy.fix_rollback()
                "Icarus menelpon Rigel, tetapi tidak ada jawaban"
                $ telpR = False
                jump telepon
            "Telepon Luna" if telpL == True:
                $ renpy.fix_rollback()
                "Icarus menelpon Luna, tetapi tidak ada jawaban"
                $ telpL = False
                jump telepon
            "Telepon Daedalus lagi" if telpD == True:
                $ renpy.fix_rollback()
                "Icarus mencoba untuk menghubungi ayahnya lagi, tetapi tidak ada jawaban"
                $ telpD = False
                jump telepon

    label doneTelepon:
        $ renpy.fix_rollback()
    hide icarus worried
    p "HEY, BOCAH! NGAPAIN KAU DI SITU"
    p "CEPAT EVAKUASI KE SHELTER TERDEKAT!"
    show icarus surprised with dissolve
    i "H-hah? Oh baiklah"
    hide icarus surprised with dissolve
    play sound "sounds/rame.mp3"
    w "HEY CEPAT BERGERAK! KAU MENGHALANGI JALAN"
    om "Mana sopan santunmu anak muda, kau tidak lihat aku ini sudah tua?!"
    ow "Oh sudahlah, sayang. Ayo kita bergegas ke shelter dengan tenang"
    bo "Huhu nenek, aku takut"
    g "Aku juga! HUAAAAHHHHH"
    ow "Oh sayang... cup cup cup..."
    show icarus worried with dissolve
    i "Nampaknya ini bencana yang sangat besar"
    i "Kuharap papa, Rigel, dan Luna baik-baik saja"
    stop sound
    stop music fadeout 1.0
    scene black with dissolve
    pause

    play music "music/Mesmerize.mp3" loop
    scene bg shelter
    "Setelah beberapa minggu rakyat Ílios berlindung di shelter tersebut, mereka mulai kehabisan stok pangan dan kebutuhan sehari-hari yang lain"
    "Negeri itu dikelilingi gurun pasir sepanjang mata memandang, dan dengan jalur komunikasi yang tidak kunjung membaik karena belum ada kesempatan untuk siapa pun untuk keluar dan memperbaiki menara komunikasi, bantuan pun belum ada yang datang"
    "Bahkan kemungkinan berbagai negara lain juga terkena gempa dahsyat tersebut mengingat tinggi gunung Ignis yang sangat raksasa itu"
    "Karena tidak ada pilihan lain, mereka semua bertekad untuk keluar dan mencari apa pun itu yang masih bisa digunakan"
    "Icarus di lain sisi, tidaklah khawatir dengan itu semua, pikirannya hanya tertuju pada teman-temannya, Rigel dan Luna, serta keluarga satu-satunya yaitu ayahnya yang mungkin saja berlindung di shelter lainnya"
    "Tetapi tetap saja tanpa adanya kabar yang pasti tentang mereka, kekhawatiran Icarus semakin membesar"

    scene bg ilios2 with dissolve
    "Ketika keluar dari shelter, bangsa Ílios mendapati negeri mereka sudah gelap gulita dan dingin, langit tertutup oleh awan hitam akibat amarah gunung Ignis"
    "Negeri matahari itu sudah tidak terang dan hangat lagi"
    "Dikarenakan bangsa itu hampir bergantung penuh kepada energi matahari, Ílios kembali krisis energi seperti 50 tahun yang lalu"

    show icarus worried
    i "UHUK UHUK"
    i "Ugh... Udaranya kotor sekali..."
    i "Hufh... Semuanya gelap... D-dan y-ya ampun... Di-dingin sekali"
    i "Tidak pernah aku seumur-umur merasakan Ílios sedingin dan segelap ini"
    hide icarus worried
    p "Hey, kau yang di situ!"
    show icarus surprised with dissolve
    i "I-iya?"
    p "Jangan bengong-bengong saja, ayo bantu warga mencari korban yang selamat atau paling tidak mencari pangan yang masih bisa dikonsumsi"
    i "Baiklah"

    scene bg ilios2 with dissolve
    "Para warga kembali meramaikan negeri itu, berlalu-lalang, mencari harta mereka yang tertinggal. Tetapi yang mereka dapatkan hanyalah tumpukan abu"
    om "Hey, anak muda.... Ambillah scanner ini, pemerintah membagi ini pada banyak rakyat untuk membantu proses pendataan warga yang selamat dan yang tidak"

    show scanner with dissolve:
        xalign 0.5 yalign 0.5

    "Scanner ini merupakan teknologi yang digunakan bangsa Ílios untuk mencatat data kesehatan warga pada database negeri itu."
    "Mesin itu tinggal di arahkan ke leher mereka dan mesin itu akan secara otomatis menunjukkan data sang pasien dan diagnosa penyakit mereka kemudian mencatatnya di database."
    "Tetapi pada kasus ini, mesin tersebut digunakan untuk mendata siapa sajakah yang masih selamat."
    hide scanner with dissolve
    "Icarus pun mengelilingi kota di mana ia tinggal, sungguh ia berharap tidak menemukan siapapun yang ia kenal di reruntuhan bangunan dan tumpukkan abu"
    play music "music/jasad.mp3" loop
    "Satu per satu warga ditemukan, scanner tersebut selalu menampilkan ID penduduk, biodata mereka, dan sebuah tulisan yang tadinya biru berubah menjadi merah--"
    play sound "sounds/pip.mp3"
    "‘MENINGGAL’..."
    "Data tersebut akan ditampilkan oleh pemerintah di townhall dengan sedikit energi yang tersisa, layar biru akan menampilkan warga yang selamat dan layar merah akan menampilkan warga yang telah meninggal dunia"

    "Ketika mengelilingi kota, ia menemukan Omegamart"
    scene bg omegamart
    show icarus neutral
    i "Mungkin masih ada sesuatu yang bisa dikonsumsi warga..."

    default minuman = False
    menu:
        "Masuk Omegamart":
            $ renpy.fix_rollback()
            scene bg dlmomegamart
            "Didapatinya di dalam Omegamart itu sudah dipenuhi abu"
            show icarus worried with dissolve
            i "Sepertinya tidak ada yang bisa kupakai ataupun konsumsi... Huft..."

            menu:
                "Keluar Omegamart":
                    $ renpy.fix_rollback()
                    "Icarus pun keluar dari Omegamart dengan tangan kosong"
                    jump keluarOmega
                "Tetap mencari di dalam":
                    $ renpy.fix_rollback()
                    hide icarus worried
                    show icarus surprised with dissolve
                    i "Sebentar.... Apa itu di bawah kolong rak?"
                    "Di bawah kolong rak itu terlihat seperti ada pantulan cahaya"
                    hide icarus surprised
                    show icarus determined with dissolve
                    i "WAH! Teh Kucup!"
                    i "Syukurlahhh, ternyata aku masih bisa minum walaupun hanya sebotol teh kucup. Kebetulan aku sedang haus sekali"
                    i "Hmmm... Tapi ku minum nanti pas istirahat sajalah... Aku harus fokus membantu warga sekarang"
                    $ minuman = True
                    jump keluarOmega
        "Tetap membantu mencari korban":
            $ renpy.fix_rollback()
            i "Ah mana mungkin setelah bencana sebesar itu masih ada produk yang bisa dikonsumsi"
            jump tidakOmega

    label keluarOmega:
        scene bg ilios2
        "Sesaat setelah icarus keluar dari omegamart dia melihat seorang nenek yang duduk lemas dipinggir jalan. Raut wajahnya menunjukkan kalau dia sangat kehausan."
        ow "...hufh"
        show icarus worried with dissolve
        if minuman == True:
            i "Nenek itu nampaknya haus sekali, apa kuberikan saja ya Teh Kucup ini...? Ta-tapi... Aku juga sangat haus"
            show screen repbar
            menu:
                "Berikan Teh Kucup ke nenek tersebut":
                    $ renpy.fix_rollback()
                    hide icarus worried
                    show icarusN flip with dissolve
                    i "Nek, nampaknya nenek haus sekali. Ini teh untukmu"
                    ow "Oh ya ampun, bagaimana kau tahu aku sedang haus? Terima kasih banyak anak muda, aku sungguh berhutang budi padamu"
                    $ currentrep +=5
                    i "Hehe sama-sama, nek~"
                    hide screen repbar
                    jump tidakOmega
                "Simpan Teh Kucupnya untuk diminum nanti":
                    $ renpy.fix_rollback()
                    $ currentrep -=5
                    "Aku sedang bekerja keras membantu warga, tugasku pasti lebih berat dari nenek itu... Sebaiknya kusimpan sajalah Teh Kucupnya"
                    hide screen repbar
                    jump tidakOmega
        else:
            i "Kasihan sekali, andai saja diriku bisa menolongnya... Tetapi tadi di Omegamart sama sekali tidak ada minuman..."

    label tidakOmega:
        $ renpy.fix_rollback()
        scene bg ilios2
        "Icarus pun lanjut mencari para korban yang selamat..."
        "Meski beberapa korban yang ditemuinya masih memiliki sedikit harapan untuk diselamatkan, tetapi tetap saja mayoritas korban yang ia temukan sudah kehilangan nyawanya"
        "Melihat banyak jasad di kota tersebut, Icarus sudah tidak kuat lagi dan langsung pergi ke town hall untuk beristirahat sebentar sekaligus mencari nama-nama dari orang-orang tersayangnya pada layar biru itu... Atau setidaknya itulah yang diharapkannya"

    scene bg townhall3
    play sound "sounds/rame.mp3"
    "Town hall sudah dikerumuni banyak masyarakat Ílios yang khawatir dengan keadaan keluarganya"
    "Mereka semua menatap kedua layar yang terpapar di sana dengan penuh harap"
    "Sebagian warga menghela nafas lega ketika menemukan nama orang-orang yang dikenalinya berada di layar biru"
    "Dan sebagian warga lainnya menangis tersedu-sedu menatap layar merah dengan nama-nama orang tersayangnya yang terpajang di situ"
    "Sementara itu, Icarus menerobos kerumunan itu untuk melihat layar yang ada"

    show icarus worried with dissolve
    i "Ayolah...Mana bagian huruf D...? Daedalus... Daedalus..."
    "Icarus terus mencari nama ayahnya yang tak kunjung ia temukan di layar biru"
    "Tangannya membeku, nafasnya tersengal, tubuhnya bergidik ketakutan"
    "Oh semoga saja nama ayahnya tidak ada di layar merah itu"
    "Dengan terpaksa, karena ia sangatlah butuh kabar pasti mengenai ayahnya, ia pun mengecek layar merah"
    i "D... D... Huruf D... Di mana sih..."
    i "Ah ini dia... Dabi... Dante... David... Doppo..."
    hide icarus worried
    show icarus sigh with dissolve
    i "Syukurlah nampaknya tidak ada nama ayahku"
    play sound "sounds/beep.mp3"
    scene bg zoomlayarmerah
    i "Ah datanya bertambah lagi!"
    i "Updatenya lama juga... Mungkin karena persediaan energi sudah menipis dan gangguan sinyal komunikasi"
    i "Mu-mungkin kucari dulu di layar biru"
    play sound "sounds/beep.mp3"
    stop music

    scene bg merahdaedalus
    i "!!!"
    i "Da-Dae....Daedalus?!"
    i "Ti-...tidak.... Ini tidak mungkin, nama Daedalus itu nama yang pasaran bukan... Bisa saja itu bukan ayahku"
    i "Mari cek ID-nya.... 105217020022023XYZ"
    scene bg tab3 with dissolve
    i "Urgh... loadingnya lama sekali"
    scene bg tab4 with dissolve
    i "AH... AKHIRNYA! Mari kita cari.... 10...5217....020022023....XYZ...."
    i "Oh papa.... Ku harap ini bukan dirimu...."
    "Icarus hanya dapat berharap"
    scene bg tab5 with dissolve
    "Tetapi harapan itu sirna"

    play music "music/Anguish.mp3" loop
    show icarus sad
    i "Pa-...Papa..."
    i "Tidak... Tidak... INI TIDAK MUNGKIN! INI PASTI SALAH! PAPAKU PASTI MASIH HIDUP!"
    i "Pasti scannernya error! A-atau ada bug pada program pendataan ini!"
    i "Hik.... I-ini... Pasti sebuah kesalahan bukan.... Ini semua pasti mimpi... Sebuah mimpi yang amat sangat buruk...."
    i "Dan sebentar lagi aku akan terbangun, menyiapkan sarapan dan cappucino kesukaan ayahku di dini hari dan kami akan bercanda seperti biasanya"
    "Senyuman yang biasa terlukis pada wajahnya hilang... Cahaya matanya memudar.... Ia merasa hidupnya sudah hancur dan tak ada harapan lagi"
    "Ayahnya adalah segalanya bagi Icarus. Karena ayahnya telah tiada, maka ia telah kehilangan segalanya."
    scene bg icarusmadesu with dissolve
    pause
    i "Oh papa... Andaikan ku tahu ini semua akan terjadi... A-aku... Aku pasti akan lebih menghargai waktu kita bersama... Aku akan menjadi anak yang lebih baik lagi"
    i "Andaikan kau tidak memaksakan untuk pergi bekerja dan pergi bersamaku ke perayaan Ílios.... Mungkin kau akan berada di sisiku sekarang... Menghiburku, memelukku, mengelus kepalaku dan berkata bahwa... bahwa... semuanya akan baik-baik saja..."


    scene bg townhall3 with dissolve
    play sound "sounds/rame.mp3"
    pause
    show rigel sad at right with dissolve
    r "Astaga lihatlah semuanya... Aku yakin lebih dari setengah negeri ini sudah tertimbun pasir dan abu..."
    r "Rumahmu... Rumahku--... Tidak... Rumah kita.... Semuanya sudah tiada"
    show lunaSad flip at left with dissolve
    l "Iya... Ílios yang kita kenal sudah tiada lagi... Hik... Hik... Huhuhuuu"
    l "Hik... Oh... Mengapa... Mengapa ini terjadi?"
    r "Lu-luna... Ayolah... Semua ini tidak apa-apa, aku yakin dalam berapa bulan kedepan perbaikan pasti sudah selesai. Kita ini tinggal di zaman modern, aku yakin penanganan bencana akan berlangsung cepat"
    r "Lagipula tadi kita sudah memeriksa di layar biru dan mengetahui sebagian besar keluarga kita selamat, orang tuamu, orang tuaku.... Ya... meski... ada beberapa--"
    hide rigel sad
    show rigel sweatdrop at right with dissolve
    r "AH SUDAHLAH JANGAN BAHAS INI LAGI... URGH.... Bikin depresi saja... Ayolah! Ayolah! Senyum sedikit untukku?"
    l "Bagaimana bisa aku tersenyum di keadaan seperti ini?"
    hide rigel sweatdrop
    show rigel neutral at right with dissolve
    r "Hey hey... Kau ingat kan tadi di layar biru terpapar nama Icarus... Setidaknya kita tahu kalau dia selamat, bagaimana kalau kita mencarinya?"
    stop music fadeout 0.1
    r "Hehe... Belom kuketekin itu anak habis membuat kita ngantri panjang buat [prod] di Stand [stand] pas perayaan tiga minggu lalu!"
    hide lunaSad flip
    show lunaSigh flip at left
    l "Hufh... Rigel kamu ini  ada-ada saja..."
    stop sound
    scene black with dissolve
    "Sementara itu di sisi lain"
    play music "music/panas2.mp3" loop fadeout 1.0
    scene bg ilios2 with dissolve
    "Pemerintah bertindak cepat untuk menanggulangi bencana tersebut, tetapi karena energi yang tersimpan pada baterai-baterai yang tersebar di negeri itu hanyalah cukup untuk satu malam, mereka tak dapat menggunakannya secara maksimal"
    "Selain itu cuaca di Negeri Ílios menjadi tidak stabil yang menyebabkan proses pertanian dan peternakan terganggu"
    "Pemerintah berusaha mencari solusi atas terjadinya krisis energi"

    show minos neutral with dissolve
    m "Bagaimana ini... Kita harus mengatasi krisis energi yang melanda bangsa ini. Krisis besar-besaran 50 tahun yang lalu seakan-akan terulang lagi"
    m " Oh apa yang akan Raja Meon lakukan pada situasi seperti ini"

    show belphegor neutral behind minos with dissolve:
        xalign 0.75
    b "OHH~ Yang Mulia, aku mempunyai ide!!! HYAKHYAKHYAK~"
    hide minos neutral with dissolve
    hide belphegor neutral with dissolve

    show minosN flip at left with dissolve
    show belphegor neutral at right with dissolve
    b "Bagaimana jika kita memanfaatkan energi batu bara yang masih ada"
    m "Bukankah energi itu sudah sangat langka dan sulit ditemukan?"
    b "Daripada kita termenung dalam krisis ini tanpa melakukan apa-apa, sebaiknya kita mencoba segala opsi yang ada, yang Mulia"
    m "Belphegor, kau benar juga! Baiklah, lakukan saja!"
    m "Yang penting rakyatku tidak menderita, kerahkan ekspedisi ke area pertambangan yang sudah lama kita tinggalkan itu! Siapa tahu saja masih ada harapan"
    b "HYAK HYAK HYAK, baiklah yang Mulia"

    scene bg gurunpasir1 with dissolve
    "Pencarian batubara akhirnya dimulai"
    "Batubara adalah bahan bakar fosil dan merupakan sisa-sisa vegetasi prasejarah yang diubah yang awalnya terakumulasi di rawa-rawa dan rawa gambut."
    "Energi yang kita dapatkan dari batu bara saat ini berasal dari energi yang diserap tanaman dari matahari jutaan tahun yang lalu\n~ World Coal Association"
    "Dikarenakan memang pertambangan-pertambangan batubara itu sudah lama ditinggalkan dan baru saja terjadi bencana, banyak area yang terlalu riskan untuk dieksplorasi"
    "Hanya ada sedikit dari sekian pertambangan yang masih dapat dieksplorasi, dan mereka perlu menggali lebih dalam untuk mendapatkan batubara yang dibutuhkan"
    "Tetapi sayang, mereka hanya menemukan segelintir sisa batu bara yang ada... Stok batubara tersebut mungkin hanya bisa dipakai dalam beberapa jam"

    stop music fadeout 1.0
    scene black with dissolve
    pause
    scene bg icarusmadesu with dissolve
    "???" "...rus"
    "???" "....carus!.... ICARUS...."
    "???" "HEY! ICARUSSSS!!!!"
    scene bg townhall3
    show icarus surprised at right
    i "H-hah?!"
    show lunaN flip at left with dissolve
    l "Hey, bumi kepada Icarus, apakah kau masih di sini?"
    i "Lu-LUNA?!"
    "Melihat sosok yang amat familiar itu, Icarus langsung bangkit berdiri"
    i "Apakah benar ini kamu"
    hide lunaN flip
    show lunaPout flip at left with dissolve
    l "Bukan. Aku Anul kembarannya Luna-- YAIYALAH AKU LUNA, SIAPA LAGI COBA"
    hide icarus surprised
    show icarus touched at right with dissolve
    i "Kau selamat, syukurlah! Bagaimana dengan Rigel? Apa dia selamat? Apakah kamu bersamanya?"
    hide icarus touched
    hide lunaPout flip
    scene bg townhall3
    r "NGGA, AKU GA SELAMAT, AKU TERPAKSA MENDERITA BUAT MENGANTRI UNTUK [verb] [prod] DI STAND [stand] PADA HARI ITU!"
    scene bg reunion with dissolve
    play music "music/Ever Mindful.mp3" loop
    i "ASDFGHJKL RIGEL! LEPASIN GAK DASAR BOCAH LUMUTAN!"
    r "G"
    l "Kalian ini ya ribut ga liat situasi kondisi ckckck..."
    r "Sini Luna kuketekkin juga"
    l "RIGEL!"
    i "Hahaha, sudah sudah"
    i "Aku benar-benar lega kalian selamat"
    r "Aww co cwit"
    i "Berisik!"
    l "Kami juga lega kamu selamat, Icarus"

    scene bg townhall3 with dissolve
    "Pada reuni tersebut Icarus menceritakan soal kematian ayahnya kepada teman-temannya"
    show luna sad at right
    l "Kami turut berduka cita Icarus"
    show rigelSigh flip at left
    r "Setidaknya kamu masih memiliki kami"
    "Luna dan Rigel tak mampu melakukan apa-apa selain menghibur Icarus dan berusaha membangkitkan semangat hidupnya"

    "Syangnya, reuni mengharukan tersebut diganggu oleh salah seorang rekan kerja Daedalus"
    hide luna sad
    hide rigelSigh flip
    s "Hey, kau Icarus kan?"
    show icarus neutral with dissolve
    i "Uh... Iya. Ada apa ya, tante? Apa saya kenal dengan Anda?"
    s "Saya ini rekan kerja Daedalus, ayahmu. Saya turut berduka cita atas kepergian ayahmu"
    i "Iya... Terima kasih"
    s "Apakah kau tahu, bahwa sebenarnya ayahmu selama ini melakukan penelitian secara diam-diam? Ia menyembunyikan banyak hal dari pemerintah dan bahkan rekan kerjanya sendiri"
    "Scientist tersebut langsung menunjukkan dokumen-dokumen bukti penelitian tersebut"
    play music "music/panas2.mp3" loop
    s "Tim saya menemukan dokumen-dokumen ini dalam brankas ayahmu di laboratorium kami. Sepertinya teknologi yang ia buat ini bisa membantu Ílios mengatasi krisis ini."
    i "Oh saya tidak mengetahui apa-apa soal itu, tapi syukurlah kalau masih ada harapan"
    s "Hmph... Jangan salah sangka, ayahmu itu menyembunyikannya dari kami semua. Hingga sekarang kami belum menemukan komponen-komponen maupun blueprint dari penemuan itu"
    s "Ku rasa kau sebagai anak dari LELAKI TIDAK TAHU DIRI itu pasti mengetahui keberadaan semua data yang kami butuhkan itu. CEPAT KATAKAN LOKASINYA, TIDAK PERLU BANYAK ALASAN"

    default kata = ""
    hide icarus neutral
    show screen repbar
    menu:
        "Ta-tapi aku benar-benar tidak tahu soal hal itu!":
            $ renpy.fix_rollback()
            s "jangan banyak alasan, kau ini anak kriminal! Ayahmu menyembunyikan informasi penting dari pemerintah, dan itu adalah tindakan kejahatan!"
            $ kata = "dia sudah bilang tidak tahu"
            jump scientistAns
        "Aku tidak perlu menjawab pada seseorang yang tidak tahu tata krama":
            $ renpy.fix_rollback()
            s "Dasar, anak dan ayah sama saja tidak tahu diri"
            $ kata = "jangan ngegas dong"
            $ currentrep -= 5
            pause
            jump scientistAns
        "Apakah Anda sudah memeriksa meja kerjanya?":
            $ renpy.fix_rollback()
            s "Anda pikir kalau saya belum memeriksanya saya akan kesini, dan berbicara pada bocah sok tahu sepertimu?! TENTU SAJA SUDAH SAYA CARI SELURUH SUDUT LABORATORIUM ITU!"
            s "Ayah dan anak sama saja bodoh!"
            $ kata = "MAKSUDMU APA"
            jump scientistAns

    label scientistAns:
        hide screen repbar
        show rigelAng flip at left
        r "Hey hey, [kata], nenek sihir! Nggak perlu maksa lah! Sampai menghina seorang almarhum pula, sepertinya malah kau yang tidak tahu diri!"

    s "Bocah, jaga mulutmu!"
    show luna sad at right with dissolve
    l "Kalian ini, jangan bertengkar!"
    l "Maaf bu, teman kami ini memang terlalu emosional, tolong jangan diambil hati"
    s "HMPH"
    s "Saya tidak mau tahu, cepat cari hasil penelitian ayahmu itu. Kalau saya tahu lokasinya, buat apa saya berbicara pada bocah rendahan sepertimu!"

    r "OH NGAJAK BERANTEM YA"
    hide luna sad
    show luna angry at right with dissolve
    l "RIGEL! SSSSHHH!"
    hide luna angry
    show luna sigh at right with dissolve
    l "Tolong lah pak, setidaknya berikan Icarus waktu. Dia baru saja kehilangan ayahnya."
    s "Jadi menurutmu satu negara ini harus menderita lebih lama demi menunggu bocah ini bangkit dari keterpurukannya? Kita ini tidak punya banyak waktu!"
    "Mendengar kata-kata tersebut Rigel mulai memanas"
    r "DA--"
    hide luna sigh
    show screen repbar
    menu:
        "Tahan Rigel":
            $ renpy.fix_rollback()
            "Icarus menahan Rigel sebelum ia bertindak gegabah"
            $ currentrep +=5
            show icarus worried at right with dissolve
            i "Derajatmu lebih tinggi dari orang itu Rigel, jangan kemakan emosi!"
            s "SEMBARANGAN SAJA NGOMONGNYA KAU!"
            jump stopRigel
        "Biarkan saja":
            $ renpy.fix_rollback()
            show luna angry at right with dissolve
            $ currentrep -= 5
            l "RIGEL!"
            "Luna menahan Rigel sebelum ia bertindak gegabah"
            s "Tch..."
            hide luna angry
            jump stopRigel

    label stopRigel:
        show luna sad at right with dissolve
        l "Tolonglah bu, berilah dia waktu...."
        hide screen repbar

    s "HUH... Baiklah, kuberi kau waktu 72 jam dari sekarang untuk mencari data-data tersebut"
    stop music fadeout 1.0

    scene black with dissolve
    pause
    play music "music/rencanabelph.mp3" fadeout 1.0
    "???" "HYAKHYAKHYAK"
    show belphegor neutral with dissolve
    b "Ku mendapat info besarrrr~"
    b "Aku dapat menggunakan informasi ini untuk mendapatkan hasil penelitian itu! Dengan begitu aku bisa memenangkan hati masyarakat!"
    b "LALU AKU TINGGAL MENYINGKIRKAN RAJA MANJA ITU"
    b "Aku hanya perlu membuatnya terlihat buruk di depan masyarakat, dengan begitu aku bisa mengambil takhta nya! HYAKHYAKHYAK"
    b "Setelah Icarus berhasil mendapatkan hasil penelitian itu, akan kurebut dari kedua tangannya!"

    scene bg townhall3 with dissolve
    show belphegor neutral with dissolve
    b "Hey, bodyguard di sebelah situ! Iya, kamu! Sini sebentar"
    b "Ikuti anak-anak itu..!!! jangan sampai ketahuan. Jika dia selesai menemukan hasil penelitian tersebut cepat katakan kepadaku dan rebut dari dia"
    bg "Untuk apa pak ?"
    b "Jangan banyak tanya, lakukan saja! ini demi keselamatan Ílios!!!"
    bg "Siap laksanakan, Boss"
    b "Mudah sekali mereka ditipu HYAKHYAKHYAK...."

    scene bg townhall3 with dissolve
    play music "music/Ever Mindful.mp3" loop
    "Sementara itu Icarus masih terlarut dalam kesedihannya. Belum ada berapa jam sejak berita duka tentang ayahnya, ia sudah disuguhi masalah baru"
    "Tanpa ada pilihan lain Icarus terpaksa mencari apa yang diinginkan oleh peneliti itu"
    show icarus sigh with dissolve
    i "Teman - teman, aku yakin kalian pasti dalam keadaan lelah dan bersedih juga, tetapi aku sangat memohon bantuan dari kalian."
    i "Maukah kalian membantuku mencari catatan penelitian ayahku?"
    show rigel angry at right with dissolve
    r "Ogah! Cari aja sendiri"
    show lunaPout flip at left with dissolve
    l "HEH! JANGAN BEGITU RIGEL! Tenang saja Icarus, jangan hiraukan perkataan Rigel, kami pasti membantumu"
    hide rigel angry
    show rigel sweatdrop at right with dissolve
    r "Oh ayolah kalian pikir aku serius apa? Santai aja kali, mana mungkin aku membiarkan temanku dalam kesusahan"
    l "Ck... Kamu ini bercanda di situasi genting seperti ini!"
    hide rigel sweatdrop
    show rigel neutral at right with dissolve
    r "Daripada kalian  cemberut terus, mending ku hibur dengan kerecehanku kan"
    l "Dasar tidak tahu situasi"
    hide icarus sigh
    show icarus touched with dissolve
    i "Wahh aku sungguh terharu T_T. Kalian benar-benar sahabat sejati ku.."
    r "Jangan lebay deh Ica. Katakan saja kemana kita akan mulai mencari nya?"
    i "Hmmm..."

    default cariRumah = False
    default cariLuarKota = False
    default cariMuseum = False
    default cariLab = False

    default hint1 = False
    default hint2 = False
    label menuCari:
        menu:
            "Mulai mencari dari rumahku saja" if cariRumah == False:
                $ renpy.fix_rollback()
                scene bg livingroom with dissolve
                $ cariRumah = True
                "Icarus, Luna, dan Rigel mulai mencari petunjuk penelitian Daedalus di rumah Icarus"
                "Mau mulai mencari dari mana kah?"
                default cariKamar = False
                default cariKerja = False
                default cariDapur = False
                label CariDalamRumah:
                    menu:
                        "Kamar Daedalus" if cariKamar == False:
                            $ cariKamar = True
                            $ renpy.fix_rollback()
                            scene bg kamardae with dissolve
                            show rigel neutral at right with dissolve
                            r "Wahh, kamar ini sudah seperti kapal pecah."
                            show lunaPout flip at left with dissolve
                            l "Jaga mulut mu Rigel."
                            r "Ayolah, ku hanya mengatakan yang sebenarnya. Tuan Daedalus juga tidak akan marah."
                            i "Sudah. Lanjut kan pencarian."
                            "Mereka pun mulai mencari-cari petunjuk yang mungkin ada di dalam kamar itu"
                            hide lunaPout flip
                            hide rigel neutral
                            label cariDalamKamar:
                                menu:
                                    "Cek bawah kasur":
                                        show luna think with dissolve
                                        l "Disini tidak ada apa-apa, icarus."
                                        hide luna think
                                        jump cariDalamKamar
                                    "Cek di lemari pakaian":
                                        show rigel sweatdrop with dissolve
                                        r "Nampaknya di sini tidak ada apa-apa...."
                                        hide rigel sweatdrop
                                        jump cariDalamKamar
                                    "Kembali ke ruang tengah":
                                        show luna sigh at right with dissolve
                                        l "Disini tidak ada apa-apa icarus."
                                        show rigelN flip at left with dissolve
                                        r "Ya. Tidak ada apapun. Lebih baik kita cari di tempat lain."
                                        show icarusN flip with dissolve
                                        i "Baiklah. Ayo keluar dari sini."
                                        hide luna sigh
                                        hide rigelN flip
                                        hide icarusN flip
                                        jump CariDalamRumah

                        "Ruang kerja Daedalus" if cariKerja == False:
                            $ cariKerja = True
                            $ renpy.fix_rollback()
                            scene bg ruangkerja with dissolve
                            show icarus neutral with dissolve
                            i "Ayo masuk, ini ruang kerja ayah ku. Mungkin kita bisa menemukan sesuatu disini."

                            "Icarus, Luna dan Rigel melakukan pencarian di ruang kerja Daedalus."

                            show rigel laugh at right with dissolve
                            r "HAHAHAHAHAHA"
                            show icarus surprised with dissolve
                            i "Apa yang lucu Rigel"
                            r "Lihat. Wajah mu di foto ini lucu sekali HAHAHA"
                            show lunaN flip at left with dissolve
                            l "Mana...mana aku ingin melihatnya."
                            hide lunaN flip
                            show lunaLaugh flip at left with dissolve
                            l "Wah Rigel benar kau lucu sekali disini Icarus HAHAHA"
                            i "Sudahlah kalian berdua. Lanjutkan misi. Jangan lakukan hal yang tidak penting."
                            l "Jangan marah Icarus. Kami hanya mengatakan yang sebenarnya."

                            hide lunaLaugh flip
                            hide rigel laugh
                            hide icarus surprised
                            "Tanpa disengaja Luna menjatuhkan foto icarus dan ayahnya."
                            play sound "sounds/pecah.mp3"

                            show luna surprised at right with dissolve
                            l "Maaf Icarus sungguh aku tidak sengaja."
                            l "Aku akan merapikannya."
                            show icarus sigh with dissolve
                            i "Tidak apa Luna."
                            show rigelN flip at left with dissolve
                            r "Mari ku bantu Luna."
                            hide luna surprised
                            show luna neutral at right with dissolve
                            l "Terimakasih"
                            hide luna neutral
                            show luna surprised at right with dissolve
                            l "Hey... Di belakang foto ini ada tulisan!"
                            l "Angka-angka apa ini?"
                            hide luna surprised
                            show luna think at right with dissolve
                            l "05-07-2102?"
                            l "10-11-2100?"
                            l "Hmmm... Bukankah 05-07-2102 itu hari ulang tahunmu Icarus?"
                            hide icarus sigh
                            show icarus neutral with dissolve
                            i "Yap, benar sekali"
                            hide luna think
                            show luna neutral at right with dissolve
                            l "Lalu bagaimana dengan 10-11-2100, Icarus?"
                            i "Oh... itu..."
                            i "Seingatku itu tanggal pernikahan kedua orang tuaku"
                            show rigelN flip at left with dissolve
                            r "Lihat apa yang ku temukan, teman-teman!"
                            r "Aku menemukan sebuah PC. Mungkin saja paman Daedalus menyimpan sesuatu didalamnya."
                            scene bg laptop1 with dissolve
                            i "Coba kita periksa."
                            play sound "sounds/beep.mp3"
                            scene bg laptop2 with dissolve
                            play music "music/mikir.mp3"
                            r "Wahh ada passwordnya."
                            l "Apakah kau tau Icarus."
                            i "Hmmm aku tidak tahu tapi mari kita coba."
                            i "Jika aku menjadi ayah. Kira-kira aku buat password apa."
                            default passwordLaptop = "10-11-2100"
                            label masukkanPass:
                                python:
                                    password = renpy.input("Password: ")
                                    password = password.strip()
                                    "Icarus mencoba mengetik [password]"
                                if password == passwordLaptop:
                                    jump passLaptopBenar
                                else:
                                    play sound "sounds/wrongpassword.mp3"
                                    "PASSWORD SALAH!"
                                    "Silahkan coba lagi"
                                    i "Tidak bisa, tulisannya salah."
                                    l "Mungkin paman akan membuat sesuatu yang sangat berarti baginya. Menurut kalian apa?"
                                    i "Sangat berarti yaa.."
                                    r "Jangan lupa pehatikan setiap karakter yang kau tulis ya, siapa tahu ada simbol yang salah"
                                    i "Baiklah, akan kucoba lagi"
                                    jump masukkanPass
                            label passLaptopBenar:
                                play music "music/Ever Mindful.mp3" loop fadein 1.0
                                scene bg laptop3 with dissolve
                                play sound "sounds/correct.mp3"
                                show icarus determined with dissolve
                                i "Wah! BERHASIL!"
                                "Icarus dan teman-temannya mulai mencari-cari data dalam laptop tersebut"
                                "Sayangnya meski sudah dibuka segala direktori yang ada, semua isi filenya hanyalah penelitian-penelitian ayahnya yang memang bersifat publik"
                                "Tidak ada sama sekali data mengenai penelitian rahasia tersebut"
                                "Hingga akhirnya---"
                                show rigel neutral at right with dissolve
                                r "Hey lihat! ada angka-angka seperti di foto tadi!"
                                $ hint1 = True
                                "115 111 108 97 114 99 101 108 108"
                                show lunaT flip at left with dissolve
                                l "Hmmm tapi kali ini tidak terlihat seperti tanggal"
                                l "Kira-kira apa maksudnya ya"
                                hide icarus determined
                                show icarus think with dissolve
                                i "Aku juga tidak tahu"
                                r "Aku yakin ini pasti sebuah petunjuk, sebaiknya kita ingat baik-baik angka-angka tersebut! Luna, bagaimana jika kau mencatatnya?"
                                hide lunaT fliip
                                show lunaN flip at left with dissolve
                                l "Ide bagus, akan kucatat angka-angka itu sekarang"
                                $ inventory.add(noteLuna1)
                                show screen inventory_button
                                i "Oke, karena itu semua sudah dicatat Luna, bagaimana jika kita cek tempat lain dulu. Siapa tahu ada petunjuk lain"
                                hide screen inventory_button
                                jump CariDalamRumah
                        "Dapur rumah" if cariDapur == False:
                            $ renpy.fix_rollback()
                            $ cariDapur = True
                            scene bg dapur with dissolve
                            "Icarus dan teman-temannya memeriksa area dapur"
                            if cariKerja == True and cariKamar == True:
                                show rigel angry at right with dissolve
                                r "ARGHHH lelahnya, sepertinya dari tadi kita hanya mendapat petunjuk yang tidak mengarah ke mana-mana"
                                show lunaAng flip at left with dissolve
                                l "SSHHH! RIGEL! Kita kan sudah memutuskan untuk membantu Icarus! Sudahlah jangan banyak mengeluh"
                                hide rigel angry
                                show rigel sweatdrop at right with dissolve
                                r "Iya iya aku tahu, aku hanya lelah sedikit"
                                hide rigel sweatdrop
                                hide lunaAng flip
                            show rigel sigh at right with dissolve
                            r "Andai saja dapur ini masih berfungsi, aku mau masak Íliosmie goreng rasa ayam bawang"
                            show lunaAng flip at left with dissolve
                            l "Rigel! Fokus dong!"
                            show icarus laugh with dissolve
                            i "Hahaha! Kamu bikin aku lapar saja"
                            i "Íliosmie di pagi hari memang matntab jiwa"
                            hide lunaAng flip
                            show lunaSigh flip at left with dissolve
                            l "Huft... Kalian ini ada-ada aja"

                            scene bg dapur with dissolve
                            "Ketika mereka sedang berbincang-bincang di dapur, Icarus mendadak menyadari sebuah benda hitam silindris yang tergeletak di pojok ruangan"
                            show draftingTube with dissolve:
                                xalign 0.5 yalign 0.5
                            "Nampaknya barang tersebut terjatuh ketika gempa beberapa minggu lalu sehingga Icarus baru menyadari keberadaan benda tersebut di rumah ini"
                            show icarusSurp flip at left with dissolve
                            i "???"
                            i "Tabung apa ini? Aku belum pernah melihat ini sebelumnya di rumah"
                            show luna neutral at right with dissolve
                            l "Oh! Aku tahu ini"
                            l "Bukan kah ini drafting tube? Semacam tempat yang digunakan oleh arsitek atau designer untuk menyimpan draft-draft rancangan mereka?"
                            hide draftingTube with dissolve
                            show rigel neutral with dissolve
                            r "Iya benar! Aku pernah melihat pamanku menggunakannya untuk menyimpan blueprint rancangan bangunan dan sebagainya"
                            i "Kalau begitu, siapa tahu saja isinya draft penelitian rahasia ayahku!"
                            "Mereka pun memeriksa isi dari drafting tube tersebut"
                            "Di dalam tersebut hanyalah berisi dua projektor hologram 3D portable yang berbentuk pipa"
                            r "Ini kan seperti yang biasa digunakan di kelas untuk presentasi"
                            i "Ayo kita nyalakan!"
                            scene bg dapurproj1 with dissolve
                            ""
                            play sound "sounds/beep.mp3"
                            scene bg kertaspeter with dissolve
                            "Ketika projektor tersebut dinyalakan muncullah sebuah layar biru berisikan gambar"
                            "Gambar tersebut mirip seperti hasil scan sebuah kertas tua dengan gambar sebuah teknologi yang misterius"
                            i "Apa ini?"
                            r "Mungkinkah ini teknologi yang diteliti ayahmu secara rahasia?"
                            l "Lihat, ada suatu daftar di situ, mungkinkah itu daftar komponen yang digunakan dalam teknologi itu?"
                            "1. Solar cell\n2. Laser\n3. Antenna"
                            i "Bisa jadi!"
                            r "Luna, catat itu!"
                            l "Siap!"
                            show screen inventory_button
                            $ inventory.add(noteLuna2)
                            show noteLuna2 with dissolve:
                                xalign 0.5 yalign 0.5
                            "Catatan itu disimpan di inventory"
                            hide noteLuna2 with dissolve
                            show icarus neutral with dissolve
                            i "Mari kita coba cari di tempat lain lagi"
                            hide screen inventory_button
                            jump CariDalamRumah
                        "Keluar" if cariKerja == True and cariKamar == True and cariDapur == True:
                            $ renpy.fix_rollback()
                            "Sepertinya sudah tidak ada yang dapat ditemukan di rumah ini lagi"
                            jump menuCari
            "Bagaimana kalau kita coba ke luar kota?" if cariLuarKota == False:
                $ renpy.fix_rollback()
                scene bg ilios2 with dissolve
                default gurun = False
                default ignis = False
                label cariLuarKota:
                    "Mulai dari mana?"
                    menu:
                        "Gurun pasir" if gurun == False:
                            $ renpy.fix_rollback()
                            default utara = False
                            default selatan = False
                            default timur = False
                            default barat = False
                            jump cariGurun
                        "Gunung Ignis" if ignis == False:
                            $ renpy.fix_rollback()
                            jump cariIgnis
                        "Kembali" if ignis == True and gurun == True:
                            jump menuCari
                label cariGurun:
                    scene bg gurunpasir1 with dissolve
                    "Mau ke arah mana?"
                    menu:
                        "Gurun pasir utara" if utara == False:
                            $ utara = True
                            $ renpy.fix_rollback()
                            scene bg gurunutara with dissolve
                            "Mereka pun mengeksplorasi gurun pasir sebelah utara"
                            show rigel surprised with dissolve
                            r "Hey! Kalian lihat itu?"
                            r "Sepertinya sebuah sumber air"
                            hide rigel surprised
                            play music "music/trivia.mp3" fadeout 1.0
                            scene bg dam with dissolve
                            show luna neutral with dissolve
                            l "Oh aku tahu apa itu~"
                            l "Aku pernah membacanya di perpustakaan nasional Ílios"
                            l "Itu adalah bendungan"
                            l "Bendungan atau dam adalah konstruksi yang dibangun untuk menahan laju air menjadi waduk, danau, atau tempat rekreasi."
                            l "Seringkali bendungan juga digunakan untuk mengalirkan air ke sebuah Pembangkit Listrik Tenaga Air."
                            l "Kebanyakan dam juga memiliki bagian yang disebut pintu air untuk membuang air yang tidak diinginkan secara bertahap atau berkelanjutan.\n~ Wikipedia"
                            show rigel sweatdrop at right with dissolve
                            r "Kau tahu banyak hal ya Luna"
                            l "Hoho iya dooonng"
                            show icarusLaugh flip at left with dissolve
                            i "Kamu selalu membuatku terkagum Luna, kamu seperti Guugle berjalan haha"
                            play music "music/Ever Mindful.mp3" loop fadein 1.0
                            r "Jadi ini bendungan ya... Tapi sepertinya PLTAnya tidak berfungsi. Huft... Letusan Ignis benar-benar merusak segalanya, ya"
                            scene bg dam with dissolve
                            show icarus neutral with dissolve
                            i "Sepertinya memang tidak ada yang bisa kita lakukan untuk menjalankan pembangkitnya"
                            i "Hmmm... Mari cek tempat lain"
                            if utara == True and barat == True and timur == True and selatan == True:
                                $ gurun = True
                                if ignis == True:
                                    $ cariLuarKota = True
                                jump cariLuarKota
                            else:
                                jump cariGurun
                        "Gurun pasir barat" if barat == False:
                            $ renpy.fix_rollback()
                            $ barat = True
                            scene bg gurunbarat
                            "Mereka pun mengeksplorasi gurun pasir sebelah barat"
                            show icarus surprised with dissolve
                            i "Hey lihat!"
                            i "Sepertinya di sana ada sesuatu"
                            "Pada padang pasir luas tersebut terlihat berbagai teknologi energi matahari yang nampaknya sudah ditinggalkan sejak lama"
                            show lunaN flip at left with dissolve
                            l "Wah wah wah... Lihatlah semua itu~"
                            show rigel sweatdrop at right with dissolve
                            play music "music/trivia.mp3"
                            r "Biar kutebak"
                            r "kau pasti tahu semua teknologi itu, ya kan Luna?"
                            l "Hehe... Tentu saja"
                            l "Aku pernah membaca semuanya di perpustakaan"
                            l "Ini semua adalah teknologi kuno energi surya yang sudah lama ditinggalkan bangsa kita pada abad ke-21"
                            scene bg parabolicthrough with dissolve
                            l "Ini adalah Parabolic Through"
                            l "Parabolic trough adalah jenis kolektor panas matahari yang lurus dalam satu dimensi dan melengkung sebagai parabola di dua lainnya, dilapisi dengan cermin logam yang dipoles."
                            l "Sinar matahari yang memasuki cermin sejajar dengan bidang simetri difokuskan di sepanjang garis fokus, di mana objek diposisikan yang dimaksudkan untuk dipanaskan.\n~Wikipedia"
                            scene bg solartower with dissolve
                            l "Kalau yang ini adalah Solar Tower"
                            l "Solar tower juga dikenal sebagai pembangkit listrik 'menara pusat' atau pembangkit tenaga atau menara listrik 'heliostat'"
                            l "Ini adalah jenis tungku surya yang menggunakan menara untuk menerima sinar matahari terfokus"
                            l "Ini menggunakan array datar, cermin bergerak (disebut heliostats) untuk memfokuskan sinar matahari pada menara kolektor (target)\n~Wikipedia"
                            scene bg solarpanel with dissolve
                            l "Solar Panel atau Panel Surya adalah kumpulan sel surya. Banyak sel surya kecil yang tersebar di area yang luas dapat bekerja bersama untuk menyediakan daya yang cukup untuk menjadi berguna"
                            l "Semakin banyak cahaya yang mengenai sel, semakin banyak listrik yang dihasilkannya"
                            show rigel neutral at right with dissolve
                            r "Hey, tadi kamu bilang teknologi ini menggunakan sel surya? Sel surya itu sama dengan solar cell, kan?"
                            show lunaN flip at left with dissolve
                            l "Benar sekali"
                            r "Luna, apa menurutmu benda ini penting? Bagaimana jika kita menyimpannya untuk digunakan nanti"
                            r "Siapa tahu saja bisa dipakai untuk memperbaiki pembangkit surya di kota atau membangun sesuatu yang lain"
                            hide lunaN flip
                            show lunaSurp flip at left with dissolve
                            l "Wah! Iya juga!"
                            l "TUMBEN KAMU PINTER, RIGEL"
                            hide rigel neutral
                            show rigel sweatdrop at right with dissolve
                            r "Enak saja, bocah satu ini!"
                            show icarus determined with dissolve
                            i "Guys, ayo kita ambil solar cellnya!"
                            show screen sunbar
                            "Icarus pun mencari solar cell yang kelihatannya masih bisa digunakan"
                            $ currentsun +=50
                            pause
                            show screen inventory_button
                            show solarcell with dissolve:
                                xalign 0.5 yalign 0.5
                            $ inventory.add(solarcell)
                            play music "music/Ever Mindful.mp3" loop fadein 1.0
                            "Salah satu komponen telah ditemukan"
                            hide solarcell with dissolve
                            hide screen sunbar
                            hide screen inventory_button
                            if utara == True and barat == True and timur == True and selatan == True:
                                $ gurun = True
                                if ignis == True:
                                    $ cariLuarKota = True
                                jump cariLuarKota
                            else:
                                jump cariGurun
                        "Gurun pasir timur" if timur == False:
                            $ renpy.fix_rollback()
                            $ timur = True
                            scene bg guruntimur with dissolve
                            "Mereka pun mengeksplorasi gurun pasir sebelah timur"
                            "Dari kejauhan mereka dapat melihat suatu tiang menjulang tinggi dilengkapi dengan baling-baling"
                            play sound "sounds/angin.mp3"
                            scene bg windturbine
                            "Angin berhembus, tapi nampaknya baling-baling itu bergeming"
                            show icarusN flip at left with dissolve
                            i "Hmmm... Bukankah itu Wind Turbine?"
                            show luna neutral at right with dissolve
                            play music "music/trivia.mp3"
                            l "Yap"
                            l "Turbin angin, seperti baling-baling pesawat terbang, berputar di udara yang bergerak dan menyalakan generator listrik yang memasok arus listrik"
                            l "Sederhananya, turbin angin adalah kebalikan dari kipas angin. Alih-alih menggunakan listrik untuk menghasilkan angin, seperti kipas angin, turbin angin menggunakan angin untuk menghasilkan listrik"
                            l "Angin akan memutar bilah, yang nantinya akan memutar poros, yang terhubung ke generator dan menghasilkan listrik.\n~Wind Energy Development Programmatic EIS"
                            l "Itu adalah definisi yang pernah kubaca dari perpustakaan nasional Ílios"
                            play music "music/Ever Mindful.mp3"
                            l "...Tapi sayangnya bangsa Ílios sangatlah jarang memakainya. Negeri kita terlalu mengandalkan energi surya"
                            show rigel sweatdrop with dissolve
                            r "Huft... Jadi itu kah sebabnya sekarang ini kita tidak dapat berkutat, karena langit telah ditutupi awan gelap dan kita tidak dapat memperoleh energi yang kita butuhkan?"
                            r "Menurutku bodoh sekali hanya berketergantungan dengan satu sumber energi"
                            l "Yah di Ílios memang sulit mendapatkan angin sih karena negeri kita sangat dipenuhi gedung-gedung yang menjulang tinggi, semua angin terhambat"
                            l "Belum lagi kita kekurangan lahan untuk pembangunan. Ílios sudah sangatlah padat, Rigel"
                            l "Wind Turbine ini dibangun begitu jauh dari area perkotaan karena memang kita tidak memiliki lahan, selain dari itu wind turbine juga membuat polusi suara yang begitu besar"
                            i "Lagipula dari segi efektifitas, sepertinya teknologi surya milik Ílios dapat menghasilkan lebih banyak energi dibandingkan teknologi angin"
                            r "Yasudahlah, kita tidak perlu mempermasalahkan ini lagi. Ayo lanjut mencari di tempat lain, di sini tidak ada apa-apa lagi"
                            stop sound
                            if utara == True and barat == True and timur == True and selatan == True:
                                $ gurun = True
                                if ignis == True:
                                    $ cariLuarKota = True
                                jump cariLuarKota
                            else:
                                jump cariGurun
                        "Gurun pasir selatan" if selatan == False:
                            $ renpy.fix_rollback()
                            scene bg gurunselatan with dissolve
                            "Mereka memutuskan untuk mengeksplorasi gurun pasir sebelah selatan"
                            "Tetapi yang mereka dapati hanyalah lahan kosong"
                            "Apa yang akan kalian lakukan?"
                            menu:
                                "Tetap mencoba mencari lebih jauh":
                                    $ renpy.fix_rollback()
                                    "Mereka pun mencoba mengeksplorasi lebih jauh"
                                    "Tetapi waktu terus berlalu dan yang mereka temui hanyalah padang pasir yang luas sepanjang mata memandang"
                                    show luna sigh at right with dissolve
                                    l "Huft... Icarus untuk apa kita berjalan sejauh ini"
                                    l "Sepertinya tidak ada apa-apa lagi di sini"
                                    show rigelSD flip at left with dissolve
                                    r "Ugh... iya Icarus..."
                                    r "Ayo putar balik dan cari di tempat lain..."
                                    menu:
                                        "Kembali":
                                            $ renpy.fix_rollback()
                                            jump cariGurun
                                        "Tetap lanjut":
                                            $ renpy.fix_rollback()
                                            show icarus worried with dissolve
                                            i "Ayolah kalian, sedikit lagi saja"
                                            i "Aku ada feeling kalau ada sesuatu di sini..."
                                            "Mereka terus berjalan semakin jauh dari area perkotaan"
                                            "Ketika mereka mulai berpikir untuk menyerah, di kejauhan terlihat sesuatu yang tak diduga"
                                            scene bg bunkerentrance with dissolve
                                            show icarusSurp flip at left with dissolve
                                            "Nampaknya ada sebuah pintu masuk rahasia"
                                            "Ketika mereka mencoba untuk membukanya, ternyata pintu masuk tersebut dikunci dengan sandi"
                                            if hint1 == True and hint2 == True:
                                                play music "music/mikir.mp3"
                                                $ selatan = True
                                                show luna neutral at right with dissolve
                                                l "Hey coba lihat catatan-catatan kita sebelumnya, ku rasa kita sudah mengumpulkan cukup petunjuk untuk memecahkan kata sandi ini"
                                                show screen inventory_button
                                                pause
                                                default passBunk = True
                                                label masukinPassBunker:
                                                    python:
                                                        passwordB = renpy.input("Password: ")
                                                        passwordB = passwordB.strip()
                                                    if passwordB == "solarcell":
                                                        play sound "sounds/correct.mp3"
                                                        "PASSWORD DITERIMA"
                                                        "Pintu bunker pun terbuka"
                                                        $ passBunk = True
                                                        jump bunker
                                                    else:
                                                        play sound "sounds/wrongpassword.mp3"
                                                        "PASSWORD SALAH"
                                                        "SIlahkan coba lagi"
                                                        show rigel sigh with dissolve
                                                        r "Coba kamu ingat-ingat lagi petunjuknya"
                                                        l "Angka-angka ini mengingatkanku pada ASCII..."
                                                        $ passBunk = False
                                                        jump masukinPassBunker
                                            else:
                                                hide icarusSurp flip
                                                show icarus worried with dissolve
                                                i "Urgh... Apa ya passwordnya? Sepertinya kita kekurangan petunjuk..."
                                                i "Mungkin kita harus kembali dan memeriksa tempat-tempat lainnya dengan lebih teliti"
                                                menu:
                                                    "Kembali ke pinggiran kota" if utara == True and barat == True and timur == True and selatan == True:
                                                        $ gurun = True
                                                        if ignis == True:
                                                            $ cariLuarKota = True
                                                        $ renpy.fix_rollback()
                                                        jump cariLuarKota
                                                    "Kembali ke gurun":
                                                        $ renpy.fix_rollback()
                                                        jump cariGurun
                                                    "Kembali ke perkotaan":
                                                        $ renpy.fix_rollback()
                                                        jump menuCari
                                    label bunker:
                                        "Setelah pintu bunker itu terbuka, dengan sedikit keraguan mereka pun masuk ke dalam."
                                        "Di dalam terdapat sebuah tangga melingkar menuju ke bawah"
                                        play music "music/bunker.mp3"
                                        scene bg tanggabunker with dissolve
                                        "Mereka pun langsung menyusuri tangga tersebut"
                                        scene bg dlmbunker with dissolve
                                        "Ruangan dalam bunker itu sangatlah gelap dan berantakan"
                                        show luna sad at right with dissolve
                                        l "Huhu... Di sini sangat menyeramkan..."
                                        show rigelLaugh flip at left with dissolve
                                        r "Hahaha, ayolah Luna, di sini hanyalah gelap sedikit. Cuma karena gelap bukan berarti tempat ini penuh dengan makhluk dari film horror kan"
                                        r "Sini, pegang tanganku! Cup cup cup"
                                        hide luna sad
                                        show luna pout at right with dissolve
                                        l "IDIH! Modus ya?!"
                                        hide rigelLaugh flip
                                        show rigelSD flip at left with dissolve
                                        r "Elah baper baper banget nih cewe satu"
                                        r "Ya udah kalo ga mau..."
                                        hide rigelSD flip
                                        show rigelLaugh flip at left with dissolve
                                        r "Nanti ada yang ngikutin dari belakang lhooo...."
                                        hide luna pout
                                        show luna sad at right with dissolve
                                        l "RIGGEEELLL! Jangan nakutin aku huhuuuu!"
                                        show icarus sigh with dissolve
                                        i "Guyyyssss... Jangan berantem terus dong..."
                                        i "Nih selama kalian berantem kayak kucing dan anjing aku telah menemukan petunjuk lain"
                                        scene bg dlmbunker with dissolve
                                        show screen inventory_button
                                        $ inventory.add(Journal2)
                                        show journal2 with dissolve:
                                            xalign 0.5 yalign 0.5
                                        "Journal 2"
                                        "2114 Maret (6 tahun lalu)\nAku sudah mulai mengembangkan konsep SPS itu. Tapi masih saja ada kesalahan yang belum terpecahkan.Aku akan mencobanya lagi.\n-D"
                                        hide journal2 with dissolve
                                        show lunaT flip at left with dissolve
                                        l "Hmmm... Apakah ini catatan ayahmu?"
                                        l "Di bawah halaman journal ini ada inisial 'D' sih..."
                                        show icarus determined at right with dissolve
                                        i "Sepertinya begitu,\nMungkin kita sudah dekat dengan penelitian rahasia ayahku itu! Ayo kita periksa bunker ini lebih dalam"
                                        hide screen inventory_button
                                        scene bg dlmbunker with dissolve
                                        "Cari ke mana?"
                                        default kiri = False
                                        default kanan = False
                                        label exploreBunker:
                                            menu:
                                                "Cek ruangan sebelah kiri" if kiri == False:
                                                    scene bg bunkerkiri with dissolve
                                                    $ renpy.fix_rollback()
                                                    $ kiri = True
                                                    "Ketika memasuki ruangan tersebut mereka melihat sebuah benda yang sangat mencolok"
                                                    show rigel surprised at right with dissolve
                                                    r "Hey, lihat! Benda apa itu?!"
                                                    show antena with dissolve:
                                                        xalign 0.5 yalign 0.5
                                                    show icarusDet flip at left with dissolve
                                                    show screen sunbar
                                                    i "Wah ini terlihat seperti benda yang digunakan pada satelit"
                                                    i "Mari kita ambil, aku yakin ini akan berguna"
                                                    show screen inventory_button
                                                    $ inventory.add(antena)
                                                    $ currentsun += 50
                                                    "Salah satu komponen telah ditemukan"
                                                    hide antena with dissolve
                                                    show luna neutral with dissolve
                                                    l "Ayo kita lanjut mencari"
                                                    hide screen inventory_button
                                                    hide screen sunbar
                                                    scene bg bunkerkiri with dissolve
                                                    jump exploreBunker
                                                "Cek ruangan sebelah kanan" if kanan == False:
                                                    $ renpy.fix_rollback()
                                                    $ kanan = True
                                                    scene bg kerjabunker with dissolve
                                                    "Ruangan di sebelah kanan bunker merupakan ruangan kerja Daedalus"
                                                    "Ruangan ini begitu kotor dan berantakan, banyak benda berserakan di sana sini"
                                                    default peti = False
                                                    label cekbunkerkerja:
                                                        menu:
                                                            "Cari dalam lemari":
                                                                $ renpy.fix_rollback()
                                                                "Icarus mencoba mencari benda-benda di dalam lemari"
                                                                "Tetapi di dalam lemari itu hanya berisi pakaian ganti Daedalus"
                                                                jump cekbunkerkerja
                                                            "Cari dalam laci":
                                                                $ renpy.fix_rollback()
                                                                "Luna mencoba mencari petunjuk apa pun itu di dalam laci"
                                                                "Tetapi hasilnya nihil"
                                                                "Di dalam laci tersebut hanya berisi alat-alat tulis yang bahkan sudah tidak dapat digunakan lagi"
                                                                jump cekbunkerkerja
                                                            "Cari di dalam peti besar" if peti == False:
                                                                $ renpy.fix_rollback()
                                                                $ peti = True
                                                                "Rigel mencoba membuka peti besar yang ada di pojok ruangan"
                                                                show rigel surprised at right with dissolve
                                                                show screen sunbar
                                                                r "Hey, lihat! Aku menemukan benda besar ini"
                                                                r "Bentuknya seperti parabola TV pra sejarah!"
                                                                show laser with dissolve:
                                                                    xalign 0.5 yalign 0.5
                                                                show screen inventory_button
                                                                $ inventory.add(laser)
                                                                "Salah satu komponen telah ditemukan"
                                                                $ currentsun +=50
                                                                show lunaSigh flip at left with dissolve
                                                                l "Huft... kau ini ya. Parabola tv itu mungkin masih digunakan seratus tahun yang lalu. DAN. ITU. BUKAN. PRA. SEJARAH"
                                                                hide rigel surprised
                                                                show rigel annoyed at right with dissolve
                                                                r "Oh ayolah, kenapa setiap aku melucu kamu malah ngomel terus"
                                                                hide lunaSigh flip
                                                                show lunaPout flip at left with dissolve
                                                                l "Ah sudahlah bicara denganmu tidak akan membawa kita ke mana-mana"
                                                                r "Iya, maaf baginda ratu..."
                                                                hide laser with dissolve
                                                                hide screen inventory_button
                                                                hide screen sunbar
                                                                scene bg kerjabunker with dissolve
                                                                show icarus determined with dissolve
                                                                i "Oke mari kita lanjutkan pencarian di tempat lain!"
                                                                jump cekbunkerkerja
                                                            "Kembali" if peti == True:
                                                                jump exploreBunker
                                                "Keluar" if kanan == True and kiri == True:
                                                    $ renpy.fix_rollback()
                                                    play music "music/Ever Mindful.mp3" loop
                                                    "Mereka memutuskan untuk keluar dari bunker setelah mendapatkan cukup banyak informasi"
                                                    jump menuCari
                                "Kembali" if gurun == False:
                                    $ renpy.fix_rollback()
                                    jump cariGurun
                label cariIgnis:
                    scene bg ignisgelap
                    "Area gunung Ignis ditutupi asap hitam yang sangat tebal"
                    "Sisa-sisa letusan besar gunung tersebut hanyalah polusi berbentuk awan hitam yang telah merampas cahaya matahari dari negeri Ílios"
                    show icarus worried with dissolve
                    i "Sepertinya kita tidak mampu mendekat ke gunung itu"
                    i "Kita sebaiknya kembali saja"
                    $ ignis = True
                    if ignis == True and gurun == True:
                        $ cariLuarKota == True
                    jump cariLuarKota
            "Mungkin kita coba cek dulu saja di museum penemuan" if cariMuseum == False:
                $ renpy.fix_rollback()
                $ cariMuseum = True
                scene bg museumbawah with dissolve
                play sound "sounds/rame.mp3"
                "Icarus dan teman-temannya mencoba untuk menyelidiki museum penemuan"
                "Bangunan tersebut sudah dipenuhi warga yang mengungsi di sana mengingat tidak sedikit rumah yang sudah tidak dapat dihuni"
                show icarus sad with dissolve
                i "Ughh... Aku jadi teringat dulu aku dan papaku sering pergi ke museum ini..."
                show lunaSad flip at left with dissolve
                l "Ohh Icarus... Aku mengerti bagaiman perasaanmu... Yang yabah ya, kami ada di sini bagimu..."
                show rigel sigh at right with dissolve
                r "Benar itu, ayolah senyum dikit napa, lihatlah dari sisi positifnya"
                r "Setidaknya kita tetap bersama"
                r "Ayo konsentrasi ke pencarian dulu"
                hide icarus sad
                show icarus sigh with dissolve
                i "Huft... Iya... Aku seharusnya konsentrasi mencari penelitian ini... Jika benar kata peneliti itu bahwa penelitian ayahku dapat menyelamatkan Ílios, kita harus cepat menemukannya"
                hide rigel sigh
                show rigel neutral at right with dissolve
                r "Ayo katakan saja kita perlu ke mana"
                default atas = False
                default bawah = False
                stop sound
                menu:
                    "Naik ke atas" if atas == False:
                        $ renpy.fix_rollback()
                        label lantaiAtas:
                            scene bg museumatas with dissolve
                            "Mereka mencari-cari area lantai atas museum dan mendapati banyak barang-barang bersejarah telah rusak"
                            "Di sana terdapat banyak pecahan kaca di sana sini"
                            show icarus neutral with dissolve
                            i "Hey Luna, hati-hati ya... sepertinya banyak pecahan kaca di sini"
                            show luna neutral at right with dissolve
                            l "Oh iya, terima kasih sudah memperingatiku"
                            show rigelSD flip at left with dissolve
                            r "Ohhh gitu yaaa... Yang disuruh hati-hati cuma Luna, kalo aku gelindingan di pecahan kaca ini gapapa gitu?"
                            hide icarus neutral
                            show icarus laugh with dissolve
                            i "HAHAHA, kamu kenapa sih? Cemburu ya? Lebay banget perasaan!"
                            hide rigelSD flip
                            show rigelLaugh flip at left with dissolve
                            r "Hey, lihat! Sekarang kamu ketawa!"
                            r "Kamu ini gampang banget dihibur ya"
                            hide luna neutral
                            show luna pout at right with dissolve
                            l "Kamu ini ikhlas ngehibur atau nggak sih..."
                            i "Hehe terima kasih, Rigel"
                            hide icarus laugh
                            show icarus determined with dissolve
                            i "Oke guys, mari kita geledah tempat ini!"
                            hide luna pout
                            show luna laugh at right with dissolve
                            l "Siap!"
                            r "Ayo"
                            $ atas = True
                            scene bg museumatas with dissolve
                            label tetapCari:
                                "Mereka mencari-cari petunjuk di setiap sudut pada lantai tersebut tapi mereka tidak menemukan apa-apa"
                            show rigel sigh with dissolve
                            r "Hey bagaimana jika kita cari di lantai lain?"
                            menu:
                                "Tetap cari di lantai ini":
                                    $ renpy.fix_rollback()
                                    jump tetapCari
                                "Turun ke lantai bawah" if bawah == False:
                                    $ renpy.fix_rollback()
                                    jump lantaiBawah
                                "Keluar" if atas == True and bawah == True:
                                    $ renpy.fix_rollback()
                                    "Mereka telah mencari-cari di segala sudut museum tapi tidak mendapatkan hasil"
                                    jump menuCari

                    "Coba cari di lantai ini" if bawah == False:
                        $ renpy.fix_rollback()
                        label lantaiBawah:
                            $ bawah = True
                            scene bg museumbawah with dissolve
                            "Mereka memutuskan untuk mencari di lantai dasar"
                            "Tetapi dikarenakan keadaan museum yang sangatlah ramai dengan warga yang mengungsi, pencarian sulit dilakukan"
                            label tetapCari2:
                                "Mereka mencari-cari petunjuk di setiap sudut pada lantai tersebut tapi mereka tidak menemukan apa-apa"
                            show rigel sigh with dissolve
                            r "Hey bagaimana jika kita cari di lantai lain?"
                            menu:
                                "Tetap cari di lantai ini":
                                    $ renpy.fix_rollback()
                                    jump tetapCari2
                                "naik ke lantai atas" if atas == False:
                                    $ renpy.fix_rollback()
                                    jump lantaiAtas
                                "Keluar" if atas == True and bawah == True:
                                    $ renpy.fix_rollback()
                                    "Mereka telah mencari-cari di segala sudut museum tapi tidak mendapatkan hasil"
                                    jump menuCari
            "Kita coba periksa lab di mana ayahku kerja saja" if cariLab == False:
                $ renpy.fix_rollback()
                scene bg laboratorium
                "Mereka memutuskan untuk mencari petunjuk di laboratorium di mana Daedalus bekerja"
                "Ke mana kah kalian akan mencari?"
                default kerjaDae = False
                default kerjaRekan = False
                default ruangDokumen = False
                label carilaboratorium:
                    play music "music/Ever Mindful.mp3"
                    menu:
                        "Ruang kerja Daedalus" if kerjaDae == False:
                            scene bg ruangkerja with dissolve
                            $ kerjaDae = True
                            $ renpy.fix_rollback()
                            "Icarus, Rigel, dan Luna memutuskan untuk mencari petunjuk di ruang kerja Daedalus"
                            "Mereka memeriksa setiap dokumen-dokumen yang ada, setiap lembar kertas yang ada, bahkan sampah-sampah berbentuk kertas lecak pun juga mereka periksa"
                            "Mereka sangatlah butuh petunjuk"
                            "Hingga akhirnya mereka menemukan sesuatu"
                            show rigel neutral at right with dissolve
                            r "Hey lihat, aku menemukan sebuah journal di kolong rak!"
                            show journal3_1 with dissolve:
                                xalign 0.5 yalign 0.5
                            show screen inventory_button
                            $ inventory.add(Journal3_1)
                            $ inventory.add(Journal3_2)
                            $ inventory.add(Journal3_3)
                            hide rigel neutral
                            "Journal 3 Page 1"
                            "2112 Juli (8 tahun lalu) - Aku merasa  masalah teknologi yang sekarang digunakan bangsa ini masih kurang memuaskan. Menurutku pasti ada cara agar Ilios mampu mendapatkan energi meski pada malam hari"
                            "Journal 3 Page 2"
                            "Setelah meneliti sekian lama, akhirnya ku menemukan solusi, tetapi diriku kekurangan banyak komponen. Sekian banyak buku kuno telah kubaca dan siapa sangka teknologi dari sekian abad lalu begitu menarik walau belum sempurna, akan ku sempurnakan"
                            "Journal 3 Page 3"
                            "Ku rasa alat photovoltaic dari panel surya bisa dipakai untuk alat ini. Kemungkinan penemuan ini bisa kugunakan untuk membuat solar power satellite agar Ílios tetap mendapatkan energi surya dalam kondisi apapun. Projek ini kusebut: SPS.11. (-D)"
                            "Di dalam journal tersebut terselip secarik kertas berisi tulisan"
                            "a = 97, A = 65, z = 122, Z = 90"
                            $ inventory.add(noteLuna3)
                            $ hint2 = True
                            hide journal3_1 with dissolve
                            show luna laugh at right with dissolve
                            l "Wah! Kerja bagus Rigel"
                            show icarus determined with dissolve
                            i "Iya, kerja bagus Rigel! Aku bahkan udah mau mati mencari-cari petunjuk di ruangan bagai kapal pecah ini."
                            i "Luna, tolong catat tulisan dari secarik kertas itu, siapa tahu saja itu penting"
                            l "Oke!"
                            show rigelLaugh flip at left with dissolve
                            r "Hohoho tentu saja, siapa dulu donggg, RIGEL!"
                            hide luna laugh
                            show luna pout at right with dissolve
                            l "..."
                            hide rigelLaugh flip
                            show rigelSD flip at left with dissolve
                            r "Hey apa maksud dari tatapan itu?"
                            i "Sudah sudah... Ayo kita periksa di tempat lain lagi"
                            hide screen inventory_button
                            jump carilaboratorium
                        "Ruang kerja scientist lain" if kerjaRekan == False:
                            $ kerjaRekan = True
                            scene bg kerjarekan with dissolve
                            show icarus worried with dissolve
                            i "Hey... tunggu, bukankah ini ruangan peneliti yang menghina papaku tadi di townhall"
                            i "Aku tidak yakin jika kita harus memeriksa ruangan ini"
                            i "Bagaimana jika dia marah dan bertindak dengan kekerasan"
                            show rigel neutral at right with dissolve
                            r "Jangan khawatir Icarus, serahkan saja padaku jika dia mulai macam-macam denganmu"
                            show lunaSigh flip at left with dissolve
                            l "Rigel... Kuharap kamu mampu mengontrol emosimu jika kita benar akan bertemu dengan peneliti tadi"
                            hide lunaSigh flip
                            show lunaN flip at left with dissolve
                            l "Tapi benar kata Rigel, kamu jangan khawatir..."
                            l "Apa pun itu, kita akan menghadapinya bersama"
                            hide icarus worried
                            show icarus neutral with dissolve
                            i "Terima kasih teman-teman"
                            scene bg kerjarekan with dissolve
                            "Mereka pun mulai mencari dokumen-dokumen bukti yang sempat ditunjukkan oleh sang peneliti itu ketika di townhall"
                            "Tidak lupa berhati-hati untuk tidak terlalu membuat banyak suara dan tidak memberantakki ruangan kerja itu"
                            show luna neutral at right with dissolve
                            l "Hey, Icarus! Lihat! Bukankah ini dokumen yang kita cari?"
                            show icarusDet flip at left with dissolve
                            i "Wah kamu benar!"
                            i "Ayo lihat apa isinya"
                            hide icarusDet flip with dissolve
                            hide luna neutral with dissolve
                            show journal1 with dissolve:
                                xalign 0.5 yalign 0.5
                            $inventory.add(Journal1)
                            show screen inventory_button
                            "Journal 1"
                            "2113 September (7 tahun lalu) - Hari ini aku berhasil menemukan sebuah konsep untuk membuat solar power satellite. Konsep ini digagas oleh Peter Glaser. Aku akan mencoba mengembangkannya. Ini akan sangat bermanfaat untuk Ílios. (-D)"
                            hide journal1 with dissolve
                            show icarus worried with dissolve
                            i "Solar Power Satellite, ya..."
                            i "Mengapa ia merahasiakan penelitian ini..."
                            hide icarus worried
                            show icarus sigh with dissolve
                            i "Huft... Mungkin aku tidak boleh terlalu memikirkannya terlalu jauh sekarang"
                            i "Baiklah apa yang harus kita lakukan sekarang?"
                            hide screen inventory_button
                            show screen repbar
                            menu:
                                "Cari lebih lanjut":
                                    $ renpy.fix_rollback()
                                    play music "music/panas2.mp3"
                                    "Icarus memutuskan untuk tetap mencari berkas pada ruangan itu dengan lebih lanjut"
                                    "Tetapi ketika mereka baru saja mau beranjak mencari petunjuk setelah membaca journal tersebut, mendadak terdengar suara langkah kaki yang mendekat"
                                    "Suara langkah kaki itu semakin terdengar"
                                    "Hingga akhirnya pintu ruangan kerja itu terbuka"
                                    s "HEY! APA-APAAN INI?!"
                                    $ currentrep -= 5
                                    show rigel surprised at right with dissolve
                                    show lunaSurp flip at left with dissolve
                                    show icarus surprised with dissolve
                                    s "SIAPA YANG MEMBERI KALIAN IZIN UNTUK MEMASUKKI RUANGAN KERJA SAYA"
                                    s "DASAR KAU INI ANAK DARI PENELITI BUSUK ITU!"
                                    "Sang peneliti nampaknya marah besar dan mulai menghampiri mereka"
                                    hide rigel surprised
                                    show rigel angry at right with dissolve
                                    r "AYO CEPAT LARI!!!"
                                    hide screen repbar
                                    scene bg kerjarekan with dissolve
                                    "Mereka langsung berlari sekencang mungkin ke arah pintu keluar, menghindari sang peneliti yang mengamuk itu"
                                    scene bg laboratorium with dissolve
                                    show luna sigh at right with dissolve
                                    l "Huft... Hah... Hah"
                                    l "Sepertinya kita sudah lari cukup jauh"
                                    hide luna sigh
                                    show lunaPout flip at left with dissolve
                                    l "Mana ya orang yang tadi bilang 'serahkan saja padaku jika peneliti itu mulai macam-macam'?"
                                    show rigel annoyed at right with dissolve
                                    r "TCH IYA MANA ITU TADI ORANGNYA"
                                    hide lunaPout flip
                                    show lunaAng flip at left with dissolve
                                    l "Kamu ini ya!"
                                    hide rigel annoyed
                                    show rigel laugh at right with dissolve
                                    r "HEHEHE, ayolah aku cuma bercanda, lagipula katamu aku harus mengendalikan emosiku"
                                    r "Daripada peneliti tadi kuajak gelut mending kita kabur aja hahaha"
                                    hide lunaAng flip
                                    show lunaSigh flip at left with dissolve
                                    l "Oh sudahlah tidak ada gunanya berbicara denganmu"
                                    l "Icarus, sebaiknya kita coba menyelidiki tempat lain lagi"
                                    jump carilaboratorium
                                "Kembali":
                                    $ renpy.fix_rollback()
                                    "Mereka memutuskan untuk keluar dari ruang kerja peneliti tersebut karena informasi yang mereka dapatkan sudahlah cukup"
                                    "Lagipula tidak baik membongkar-bongkar ruangan seseorang sejauh itu tanpa izin, pikir mereka"
                                    hide screen repbar
                                    jump carilaboratorium
                        "Ruang dokumen" if ruangDokumen == False:
                            $ renpy.fix_rollback()
                            $ ruangDokumen = True
                            scene bg laboratorium with dissolve
                            "Mereka mulai berjalan ke arah ruang dokumen"
                            "Sesampainya di depan ruang dokumen, didapatinya pintu ruangan tersebut terkunci"
                            show icarus sigh with dissolve
                            i "Sepertinya di sini hanyalah jalan buntu"
                            i "Ayo kembali ke tempat tadi saja"
                            jump carilaboratorium
                        "Keluar" if ruangDokumen == True and kerjaDae == True and kerjaRekan == True:
                            $ cariLab = True
                            $ renpy.fix_rollback()
                            jump menuCari
            "Coba rakit teknologi hasil penelitian Daedalus" if currentsun >= 150:
                scene bg perumahan2 with dissolve
                "Setelah sekian lama mencari akhirnya semua komponen yang dibutuhkan untuk salah satu teknologi hasil penelitian Daedalus pun terkumpul"
                "Icarus, Luna, dan Rigel mulai memikirkan cara untuk merakit teknologi tersebut"
                show icarus determined with dissolve
                i "Baiklah guys, mari kita coba rakit mesin ini!"
                scene black with dissolve
                play music "music/rencanabelph.mp3"
                show belphegor neutral with dissolve
                b "HYAKHYAKHYAKHYAK"
                b "AWWW SELAMAT! SELAMAT!"
                b "Sungguh kerja yang bagus, kalian telah menemukan semua komponen dari solar power satellite"
                show belphegor neutral at right with dissolve
                b "Tetapi sayang sekali"
                b "ICARUS: CHILD OF THE SUN VERSI DEMO HANYA SAMPAI DI SINI!"
                b "HYAKHYAKHYAK"
                hide belphegor neutral with dissolve
                show belphegorN flip at left with dissolve
                b "Aku yakin kalian sangat tertarik... Oh iyaaa sangatlah tertarik"
                b "Jika kalian ingin mengetahui keberlangsungan cerita ini hingga ankhir, silahkan BELI FULL VERSIONNYA"
                b "Dengan begitu, saya ucapkan adieu~"
                scene black with dissolve

    return

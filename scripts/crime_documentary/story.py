"""D.B. Cooper belgeseli: sahne listesi ve Türkçe anlatım metni.

Her sahne bir görsel tanımı (type + alanlar) ve o sahne boyunca okunacak
anlatım metninden oluşur. render.py bu listeyi sırayla seslendirir, görseli
üretir ve videoyu birleştirir.
"""

TITLE = "Gökyüzünde Kaybolan Adam: D.B. Cooper"

SCENES = [
    # --- GİRİŞ / KANCA ---
    {
        "type": "plane",
        "caption": "24 KASIM 1971 · 20:13",
        "text": (
            "Saat akşamın sekizini on üç geçiyor. Gece karanlık, yağmur çiseliyor ve hava buz gibi. "
            "Üç bin metre yükseklikte uçan bir yolcu uçağının arka merdiveni açık. "
            "Ve o merdivenin ucunda, takım elbiseli, kravatlı bir adam duruyor. "
            "Sırtında bir paraşüt, beline bağlı bir torbada iki yüz bin dolar var."
        ),
    },
    {
        "type": "title",
        "title": "GÖKYÜZÜNDE\nKAYBOLAN ADAM",
        "subtitle": "D.B. COOPER DOSYASI",
        "text": (
            "Birkaç saniye sonra adam karanlığa atlıyor. Ve bir daha asla görülmüyor. "
            "Elli yılı aşkın süredir FBI, amatör dedektifler ve gazeteciler aynı soruyu soruyor: "
            "Bu adam kimdi? Atlayışta öldü mü, yoksa kusursuz bir suçun sahibi olarak ömrünü sessizce mi tamamladı? "
            "Bu, Amerikan tarihinin çözülemeyen tek uçak kaçırma vakasının hikâyesi."
        ),
    },
    # --- BÖLÜM 1: BİLET ---
    {
        "type": "chapter",
        "num": "BÖLÜM 1",
        "title": "BİLET",
        "text": "Her şey, sıradan bir bayram arifesinde, sıradan bir havalimanında başladı.",
    },
    {
        "type": "date",
        "big": "PORTLAND",
        "small": "OREGON · 24 KASIM 1971 · ŞÜKRAN GÜNÜ AREFESİ",
        "text": (
            "Yirmi dört Kasım bin dokuz yüz yetmiş bir. Amerika'da Şükran Günü'nün arifesi. "
            "Portland Havalimanı'nda insanlar bayram için ailelerinin yanına dönmeye çalışıyor. "
            "Kalabalığın arasında kimsenin dikkatini çekmeyen bir adam, Northwest Orient Havayolları'nın gişesine yaklaşıyor."
        ),
    },
    {
        "type": "ticket",
        "name": "DAN COOPER",
        "route": "PORTLAND  →  SEATTLE",
        "flight": "UÇUŞ 305",
        "price": "$18.52",
        "text": (
            "Kendini Dan Cooper olarak tanıtıyor. Seattle'a giden üç yüz beş sefer sayılı uçuş için tek yön bir bilet alıyor "
            "ve on sekiz dolar elli iki senti nakit ödüyor. Kimlik soran yok. O yıllarda havalimanlarında güvenlik taraması diye bir şey yok."
        ),
    },
    {
        "type": "profile",
        "name": "YOLCU: DAN COOPER",
        "lines": [
            "Yaş: 40'lı yaşların ortası",
            "Boy: yaklaşık 1.80 m",
            "Koyu takım elbise, beyaz gömlek",
            "İnce siyah kravat, yağmurluk",
            "Elinde: siyah evrak çantası",
        ],
        "text": (
            "Görgü tanıklarına göre kırklı yaşlarının ortasında, bir seksen boylarında, sakin ve kibar bir adam. "
            "Koyu renk bir takım elbise, beyaz bir gömlek ve ince siyah bir kravat takıyor. Elinde siyah bir evrak çantası var. "
            "Uçağın arka sıralarından birine oturuyor, bir sigara yakıyor ve hostesten burbon ile soda istiyor. "
            "Tamamen sıradan bir iş adamı görüntüsü."
        ),
    },
    # --- BÖLÜM 2: NOT ---
    {
        "type": "chapter",
        "num": "BÖLÜM 2",
        "title": "NOT",
        "text": "Ama bu adamın cebinde, her şeyi değiştirecek küçük bir kâğıt parçası vardı.",
    },
    {
        "type": "note",
        "lines": ["Hanımefendi,", "çantamda bir bomba var.", "Yanıma oturmanızı", "istiyorum."],
        "text": (
            "Uçak kalkıştan kısa bir süre sonra, adam hostes Florence Schaffner'a katlanmış bir not uzatıyor. "
            "Florence, yalnız seyahat eden erkek yolcuların ona telefon numarası verdiğine alışkın. Notu açmadan cebine koyuyor. "
            "Adam ona doğru eğiliyor ve sakin bir sesle fısıldıyor: Hanımefendi, o nota baksanız iyi olur. Çantamda bir bomba var."
        ),
    },
    {
        "type": "bomb",
        "text": (
            "Florence yanına oturuyor. Adam evrak çantasını hafifçe aralıyor. İçeride kırmızı silindirler, kablolar ve büyük bir pil görünüyor. "
            "Bunun gerçek bir bomba olup olmadığını bugün hâlâ kimse bilmiyor. Ama o an, otuz altı yolcu ve altı mürettebatla dolu bir uçakta, "
            "kimse bunu test etmeye cesaret edemezdi."
        ),
    },
    {
        "type": "list",
        "title": "TALEPLER",
        "items": [
            "$200.000 nakit — Amerikan doları",
            "4 adet paraşüt",
            "Seattle'da bekleyen bir yakıt kamyonu",
        ],
        "text": (
            "Ardından taleplerini sıralıyor. İki yüz bin dolar, Amerikan doları olarak, nakit. Dört adet paraşüt: ikisi sırt, ikisi göğüs paraşütü. "
            "Ve Seattle'a indiklerinde uçağı doldurmak için hazır bekleyen bir yakıt kamyonu. "
            "Bugünün parasıyla bu, bir buçuk milyon dolardan fazlasına denk geliyor."
        ),
    },
    {
        "type": "fact",
        "big": "4",
        "small": "PARAŞÜT",
        "text": (
            "Dört paraşüt talebi, aslında çok zekice bir hamleydi. FBI, adamın bir rehineyi yanında atlatabileceğini düşünmek zorunda kalacaktı. "
            "Bu da onlara bozuk, sabote edilmiş bir paraşüt vermeyi imkânsız hâle getiriyordu. "
            "Cooper, daha ilk dakikadan karşısındakilerin bir adım önündeydi."
        ),
    },
    # --- BÖLÜM 3: SEATTLE ---
    {
        "type": "chapter",
        "num": "BÖLÜM 3",
        "title": "SEATTLE",
        "text": "Sonraki iki saat, havacılık tarihinin en tuhaf bekleyişlerinden biri olacaktı.",
    },
    {
        "type": "plane",
        "caption": "SEATTLE ÜZERİNDE · BEKLEME TURU",
        "text": (
            "Pilot William Scott, uçağı Seattle üzerinde daire çizerek bekletiyor. Yolculara sadece küçük bir teknik arıza olduğu söyleniyor. "
            "İnanılmaz ama yolcuların neredeyse hiçbiri, uçağın kaçırıldığını fark etmiyor. "
            "Bu sırada yerde, FBI ve havayolu şirketi büyük bir telaşla parayı ve paraşütleri toplamaya çalışıyor."
        ),
    },
    {
        "type": "money",
        "text": (
            "FBI, iki yüz bin doları on bin adet yirmi dolarlık banknot olarak hazırlıyor. "
            "Ve burada kritik bir adım atılıyor: Her bir banknotun seri numarası tek tek mikrofilme çekiliyor. "
            "Para nereye giderse gitsin, bir gün ortaya çıkarsa izini sürebilmek için."
        ),
    },
    {
        "type": "date",
        "big": "17:39",
        "small": "SEATTLE-TACOMA HAVALİMANI · İNİŞ",
        "text": (
            "Saat beşi otuz dokuz geçe uçak Seattle'a iniyor. Cooper, uçağın ışıksız ve uzak bir pist köşesine çekilmesini istiyor. "
            "Para çantası ve paraşütler uçağa getiriliyor. Karşılığında otuz altı yolcu ve iki hostes serbest bırakılıyor. "
            "Uçakta sadece pilot, yardımcı pilot, uçuş mühendisi ve hostes Tina Mucklow kalıyor."
        ),
    },
    # --- BÖLÜM 4: ATLAYIŞ ---
    {
        "type": "chapter",
        "num": "BÖLÜM 4",
        "title": "ATLAYIŞ",
        "text": "Ve şimdi Cooper'ın asıl planı ortaya çıkıyordu. Bu plan, uçağı ve uçmayı çok iyi bilen birinin planıydı.",
    },
    {
        "type": "list",
        "title": "UÇUŞ TALİMATLARI",
        "items": [
            "Hedef: Mexico City",
            "Yükseklik: 3.000 m altında",
            "Düşük hız · flaplar 15°",
            "İniş takımları açık",
            "Arka merdiven: açılabilir",
        ],
        "text": (
            "Cooper, Meksiko'ya gitmek istediğini söylüyor. Ama talimatları çok spesifik: Uçak üç bin metrenin altında, mümkün olan en düşük hızda uçacak. "
            "Flaplar on beş derece açık olacak, iniş takımları indirilmiş kalacak. "
            "Ve en önemlisi: Uçağın arka merdiveni uçuş sırasında açılabilecek. "
            "Boeing yedi yüz yirmi yedi, arka kısmından merdiven indirilebilen nadir yolcu uçaklarından biriydi. Cooper bunu biliyordu."
        ),
    },
    {
        "type": "map",
        "text": (
            "Yakıt ikmali için Reno'da bir ara iniş yapılması kararlaştırılıyor. Saat yedi kırkta uçak tekrar havalanıyor. "
            "Arkasında, karanlıkta onu takip eden askeri jetler var. Ama uçak o kadar yavaş uçuyor ki, jetler bile ona ayak uydurmakta zorlanıyor. "
            "Cooper, hostes Tina'yı kokpite gönderiyor ve perdeyi kapatıyor. Artık kabinde yalnız."
        ),
    },
    {
        "type": "date",
        "big": "20:13",
        "small": "KOKPİTTE ANİ BİR SARSINTI",
        "text": (
            "Saat sekize doğru kokpitte bir uyarı ışığı yanıyor: Arka merdiven açıldı. "
            "Ve tam olarak saat sekizi on üç geçe, uçağın kuyruğunda ani bir yükselme hissediliyor. Sanki bir yük aniden boşalmış gibi. "
            "Mürettebat bunun ne anlama geldiğini çok sonra anlayacaktı. O an, Dan Cooper fırtınalı gecede, Washington eyaletinin ormanlık arazisi üzerine atlamıştı."
        ),
    },
    {
        "type": "list",
        "title": "UÇAKTA KALANLAR",
        "items": [
            "Siyah klipsli bir kravat",
            "Sedef işlemeli kravat iğnesi",
            "Kullanılmamış 2 paraşüt",
            "8 sigara izmariti",
        ],
        "text": (
            "Uçak saat onu çeyrek geçe Reno'ya iniyor. Silahlı polisler kabine giriyor. Ama içeride kimse yok. "
            "Cooper gitmiş. Geriye bıraktıkları ise şunlar: Siyah, klipsli bir kravat, bir kravat iğnesi, kullanılmamış iki paraşüt ve birkaç sigara izmariti. "
            "Ve işin ilginç yanı, geride bıraktığı paraşütlerden biri, dikişleri kapatılmış, işe yaramaz bir eğitim paraşütüydü."
        ),
    },
    # --- BÖLÜM 5: AV ---
    {
        "type": "chapter",
        "num": "BÖLÜM 5",
        "title": "AV",
        "text": "Ertesi sabah, Amerikan tarihinin en büyük insan avlarından biri başladı.",
    },
    {
        "type": "fact",
        "big": "NORJAK",
        "small": "FBI DOSYA KOD ADI · 45 YIL SÜREN SORUŞTURMA",
        "text": (
            "FBI, davaya Norjak adını veriyor. Askerler, polisler ve gönüllüler, atlayışın gerçekleştiği tahmin edilen bölgede haftalarca arama yapıyor. "
            "Ormanlar, nehirler, göller taranıyor. Helikopterler, dağlık arazide en ufak bir paraşüt kumaşı izi arıyor. "
            "Ama ne bir paraşüt, ne bir ceset, ne de paranın tek bir kuruşu bulunabiliyor."
        ),
    },
    {
        "type": "quote",
        "quote": "D.B. COOPER",
        "who": "Bir muhabir hatasıyla doğan efsanevi isim",
        "text": (
            "Peki, D.B. Cooper ismi nereden geliyor? Aslında hiçbir yerden. "
            "Soruşturmanın ilk günlerinde polis, Portland'da yaşayan D.B. Cooper adında bir adamı kısa süreliğine sorguluyor. Adam masum çıkıyor ve hemen serbest bırakılıyor. "
            "Ama bir muhabir bu ismi haberine yazıyor ve basın onu sahiplenince isim bir anda efsaneye dönüşüyor. "
            "Kaçırıcı hiçbir zaman D.B. demedi. O sadece Dan Cooper'dı."
        ),
    },
    # --- BÖLÜM 6: PARA ---
    {
        "type": "chapter",
        "num": "BÖLÜM 6",
        "title": "NEHİR KIYISI",
        "text": "Dokuz yıl boyunca hiçbir iz çıkmadı. Ta ki sekiz yaşında bir çocuk, bir piknik sırasında kuma kazı yapana kadar.",
    },
    {
        "type": "date",
        "big": "ŞUBAT 1980",
        "small": "COLUMBIA NEHRİ · TENA BAR",
        "text": (
            "Şubat bin dokuz yüz seksen. Brian Ingram adında sekiz yaşındaki bir çocuk, ailesiyle birlikte Columbia Nehri kıyısında, Tena Bar denilen kumsalda piknik yapıyor. "
            "Kamp ateşi için kumu düzlerken eline çürümüş, lastik bantlarla tutturulmuş para desteleri geliyor."
        ),
    },
    {
        "type": "fact",
        "big": "$5.800",
        "small": "SERİ NUMARALARI EŞLEŞTİ",
        "text": (
            "Toplam beş bin sekiz yüz dolar. FBI seri numaralarını kontrol ediyor ve sonuç kesin: Bu para, Cooper'a verilen fidyenin bir parçası. "
            "Ama bu keşif, soruları çözmek yerine çoğaltıyor. Para, atlayış bölgesinden kilometrelerce uzakta bulunmuştu. "
            "Nehir mi taşıdı? Birisi oraya mı gömdü? Cooper parayı düşürdü mü? Ve geri kalan yüz doksan dört bin dolar nerede?"
        ),
    },
    {
        "type": "fact",
        "big": "$194.200",
        "small": "HÂLÂ KAYIP",
        "text": (
            "Bugün bile o seri numaraları kayıt altında. Ama aradan geçen onca yılda, geri kalan banknotlardan tek bir tanesi bile ne bir bankada, ne bir kasada ortaya çıktı. "
            "Bu, iki ihtimalden birini gösteriyor: Ya para hiç harcanmadı, ya da Cooper onu harcamaya hiç fırsat bulamadı."
        ),
    },
    # --- BÖLÜM 7: ŞÜPHELİLER ---
    {
        "type": "chapter",
        "num": "BÖLÜM 7",
        "title": "ŞÜPHELİLER",
        "text": "Peki, en güçlü şüpheliler kimlerdi?",
    },
    {
        "type": "profile",
        "name": "RICHARD McCOY",
        "lines": [
            "Vietnam gazisi, eski asker paraşütçü",
            "Nisan 1972: neredeyse aynı kaçırma",
            "Fidye: $500.000 · paraşütle atladı",
            "Yakalandı, hapisten kaçtı",
            "1974'te FBI ile çatışmada öldü",
        ],
        "text": (
            "İlk isim Richard McCoy. Cooper olayından sadece beş ay sonra, Nisan bin dokuz yüz yetmiş ikide, McCoy neredeyse aynı yöntemle bir uçak kaçırıyor. "
            "Beş yüz bin dolar alıyor ve arka merdivenden paraşütle atlıyor. Ama birkaç gün içinde yakalanıyor. "
            "Hapisten kaçıyor ve iki yıl sonra FBI ajanlarıyla girdiği çatışmada hayatını kaybediyor. "
            "Ancak tanıklar, McCoy'un Cooper'a benzemediğini söylüyor."
        ),
    },
    {
        "type": "profile",
        "name": "ROBERT RACKSTRAW",
        "lines": [
            "Vietnam gazisi, paraşüt eğitimi",
            "Pilot lisansı, patlayıcı deneyimi",
            "Belgesel ekibi tarafından suçlandı",
            "Hep inkâr etti · 2019'da öldü",
        ],
        "text": (
            "İkinci isim Robert Rackstraw. Vietnam gazisi, paraşüt eğitimi almış, pilot lisanslı ve patlayıcılarla çalışmış biri. "
            "Bağımsız bir araştırma ekibi, yıllarca onun Cooper olduğunu iddia etti. Rackstraw ise bu iddiayı hem doğruladı gibi göründü, hem de hep inkâr etti. "
            "İki bin on dokuzda öldü ve sırrını, eğer bir sırrı varsa, mezarına götürdü."
        ),
    },
    {
        "type": "quote",
        "quote": "“Ben Dan Cooper'ım.”",
        "who": "— Duane Weber'in ölüm döşeğinde eşine söylediği iddia edilen sözler",
        "text": (
            "Ve belki de en ürpertici olanı: Duane Weber. Bin dokuz yüz doksan beşte, ölüm döşeğinde eşine dönüp şunu söylediği iddia ediliyor: Ben Dan Cooper'ım. "
            "Eşi o an bunun ne anlama geldiğini bilmiyordu. Ama sonradan araştırdığında, kocasının geçmişindeki tuhaf ayrıntıların hikâyeyle örtüştüğünü fark etti. "
            "Yine de DNA ve parmak izi testleri, Weber'i kesin olarak doğrulamaya yetmedi."
        ),
    },
    # --- BÖLÜM 8: KRAVAT ---
    {
        "type": "chapter",
        "num": "BÖLÜM 8",
        "title": "KRAVAT",
        "text": "Elimizdeki en somut kanıt ise, onun uçakta bıraktığı o siyah kravattı.",
    },
    {
        "type": "tie",
        "text": (
            "FBI, iki binli yıllarda kravattan kısmi bir DNA profili çıkarmayı başarıyor. Ama eşleştirecek bir şüpheli bulunamıyor. "
            "İki bin on yedide ise bağımsız bir bilim ekibi, kravatın üzerinde milyonlarca mikroskobik parçacık tespit ediyor. "
            "Bunların arasında saf titanyum parçacıkları da var. Bin dokuz yüz yetmişlerde saf titanyum son derece nadir bir maddeydi. "
            "Neredeyse sadece havacılık ve uzay sanayisinde kullanılıyordu."
        ),
    },
    {
        "type": "fact",
        "big": "Ti",
        "small": "SAF TİTANYUM · HAVACILIK SANAYİSİ",
        "text": (
            "Bu da yeni bir teoriyi doğurdu: Cooper, belki de bir havacılık fabrikasında, örneğin Seattle bölgesindeki dev uçak üreticilerinden birinde çalışan bir mühendis ya da teknisyendi. "
            "Bu, onun uçağı neden bu kadar iyi tanıdığını, arka merdiveni nasıl bildiğini ve flap ayarlarını neden bu kadar kesin verdiğini açıklayabilirdi."
        ),
    },
    # --- BÖLÜM 9: MİRAS ---
    {
        "type": "chapter",
        "num": "BÖLÜM 9",
        "title": "MİRAS",
        "text": "Cooper'ın atlayışı sadece bir suç değildi. Havacılık dünyasını sonsuza dek değiştirdi.",
    },
    {
        "type": "list",
        "title": "COOPER'IN MİRASI",
        "items": [
            "1972: onlarca taklitçi uçak kaçırma",
            "Havalimanlarında zorunlu güvenlik taraması",
            "Bagaj ve yolcu x-ray kontrolü",
            "“Cooper Kanadı”: uçuşta merdiveni kilitleyen parça",
        ],
        "text": (
            "Olaydan sonraki yıl, Amerika'da onlarca taklitçi uçak kaçırma girişimi yaşandı. Bunun üzerine havalimanlarında yolcu ve bagaj taraması zorunlu hâle getirildi. "
            "Bugün havalimanında x-ray cihazından geçerken, aslında biraz da Cooper'ın mirasıyla karşılaşıyorsunuz. "
            "Ayrıca Boeing yedi yüz yirmi yedilere, uçuş sırasında arka merdivenin açılmasını engelleyen küçük bir mekanik parça eklendi. Adı da Cooper kanadı oldu."
        ),
    },
    # --- KAPANIŞ ---
    {
        "type": "list",
        "title": "TEORİLER",
        "items": [
            "Atlayışta öldü, cesedi hiç bulunamadı",
            "Hayatta kaldı, yeni bir kimlikle yaşadı",
            "Parayı gömdü ama geri dönemedi",
            "Bir içeriden biriydi",
        ],
        "text": (
            "Peki gerçekte ne oldu? FBI'ın kendi görüşü, Cooper'ın o geceyi büyük ihtimalle atlatamadığı yönünde. "
            "Yağmurlu bir gece, karanlık bir orman, eksi derecelerde rüzgâr ve ayağında sadece sıradan deri ayakkabılar. "
            "Ama o zaman bir soru kalıyor: Eğer öldüyse, neden ne cesedi, ne paraşütü, ne de çantası hiç bulunamadı?"
        ),
    },
    {
        "type": "title",
        "title": "DAVA\nHÂLÂ AÇIK",
        "subtitle": "SİZCE D.B. COOPER KİMDİ?",
        "text": (
            "Belki de bir yerde, bir tavan arasında, eski bir sandığın içinde, yarım asırdır kimsenin dokunmadığı yirmi dolarlık banknotlar duruyor. "
            "Belki de Cooper, bu hikâyenin efsaneye dönüşmesini uzaktan izleyerek yaşlandı. "
            "Siz ne düşünüyorsunuz? D.B. Cooper o gece öldü mü, yoksa kusursuz suçu mu işledi? Düşüncelerinizi yorumlarda yazın. "
            "Ve bu tür çözülemeyen gizemler için kanala abone olmayı unutmayın."
        ),
    },
]

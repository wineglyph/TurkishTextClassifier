"""
Turkish Text Classification Dataset Generator
Generates a balanced, realistic, diverse Turkish dataset for:
1. Soru (Question)
2. Şikâyet (Complaint)
3. Öneri (Suggestion)

Domains:
- E-ticaret / Alışveriş
- Bankacılık & Finans
- Telekomünikasyon / İnternet
- Yazılım, Mobil Uygulama & Web
- Ulaşım & Seyahat
- Sağlık & Randevu Sistemleri
- Belediye & Kamu Hizmetleri
- Kargo & Lojistik
- Eğitim & Üniversite
- Yeme-İçme & Restoran
"""

import os
import random
import re
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# Domain vocabulary & entities
DOMAINS = {
    "eticaret": {
        "items": ["siparişim", "kargom", "aldığım mont", "telefon kılıfı", "kablosuz kulaklık", "ayakkabı", "kitap seti", "akıllı saat", "kahve makinesi", "oyuncu koltuğu"],
        "actions": ["teslimat", "iade işlemi", "değişim süreci", "taksitlendirme", "hediye paketi", "fatura kesimi", "garanti belgesi"],
        "places": ["sipariş sayfasında", "kargo takip ekranında", "sepetim", "ödeme adımında"]
    },
    "banka": {
        "items": ["kredi kartım", "vadeli hesabım", "banka kartı", "EFT talimatım", "kredi başvurum", "otomatik ödeme talimatı", "sanal kartım", "pos cihazı", "mobil bankacılık şifrem"],
        "actions": ["para transferi", "limit artırımı", "faiz hesaplama", "kart yenileme", "aidat iadesi", "şifre bloke kaldırma"],
        "places": ["ATM'de", "mobil şubede", "internet bankacılığında", "hesap özetimde"]
    },
    "telekom": {
        "items": ["ev internetim", "mobil hattım", "fiber modem", "tarife paketim", "ek internet paketi", "taahhüt sürem", "e-SIM kartım"],
        "actions": ["hat taşıma", "hız testi", "fatura detaylandırma", "bağlantı onarımı", "paket yükseltme", "altyapı sorgulama"],
        "places": ["müşteri hizmetlerinde", "mobil uygulamada", "faturamda", "modem arayüzünde"]
    },
    "yazilim": {
        "items": ["mobil uygulama", "web arayüzü", "son güncelleme", "üye girişi sayfası", "profil düzenleme ekranı", "arama çubuğu", "bildirim sistemi", "şifre sıfırlama bağlantısı"],
        "actions": ["dosya yükleme", "veri senkronizasyonu", "oturum açma", "şifre değiştirme", "rapor dışa aktarma", "karanlık mod geçişi"],
        "places": ["ana sayfada", "ayarlar menüsünde", "dashboard üzerinde", "giriş ekranında"]
    },
    "ulasim": {
        "items": ["uçak biletim", "tren seferi", "otobüs koltuğum", "valizim", "aktarma bileti", "metro kartım", "feribot biletim"],
        "actions": ["bilet açığa alma", "rötar bilgilendirmesi", "koltuk seçimi", "bagaj teslimi", "check-in işlemi", "sefer iptali"],
        "places": ["otogarda", "havaalanında", "bilet satış gişesinde", "istasyonda"]
    },
    "saglik": {
        "items": ["hastane randevum", "kan tahlili sonucum", "doktor reçetesi", "MR raporum", "diş randevum", "aşı kartım"],
        "actions": ["randevu iptali", "sonuç sorgulama", "doktor konsültasyonu", "sevk işlemi", "sağlık raporu alma"],
        "places": ["poliklinikte", "MHRS sisteminde", "laboratuvarda", "danışma masasında"]
    },
    "belediye": {
        "items": ["mahallemizdeki yol", "sokak aydınlatması", "çöp konteyneri", "belediye otobüsü", "çocuk parkı", "kaldırım taşları", "içme suyu şebekesi"],
        "actions": ["asfalt çalışması", "park bakımı", "ilaçlama hizmeti", "çöp toplama", "sefer sıklığı artırımı", "sokak hayvanları tedavisi"],
        "places": ["ana caddede", "park alanında", "otobüs durağında", "mahalle meydanında"]
    },
    "kargo": {
        "items": ["gönderim", "kargo kolisini", "adrese teslim paket", "kurye teslimatı", "kırılacak eşya kolisi", "evrak zarfı"],
        "actions": ["şubeden teslim", "adres yönlendirme", "kargo takip numarası alma", "hasar tespit tutanağı", "kapıda ödeme"],
        "places": ["dağıtım merkezinde", "kargo şubesinde", "kapıda", "aktarma merkezinde"]
    },
    "egitim": {
        "items": ["ders kaydım", "harç ödemesi", "öğrenci belgem", "transkript", "vize sınav takvimi", "üniversite kütüphanesi", "akademik danışmanım"],
        "actions": ["burs başvurusu", "staj kabul belgesi", "öğrenci işleri onayı", "tez teslimi", "kayıt dondurma"],
        "places": ["öğrenci bilgi sisteminde (OBS)", "öğrenci işlerinde", "kütüphanede", "sınav salonunda"]
    },
    "restoran": {
        "items": ["yemek siparişim", "lahmacun menüsü", "pizza siparişi", "öğle yemeği", "içecekler", "tatlı menüsü"],
        "actions": ["temassız teslimat", "sipariş notu ekleme", "fiş/fatura isteme", "sos seçimi", "sıcak teslimat"],
        "places": ["restoranda", "sipariş uygulamasında", "masada", "kapıda"]
    }
}

# --- TEMPLATE DEFINITIONS ---
# For Soru (Question)
QUESTION_TEMPLATES = [
    # Direct questions with question words
    "{item} için {action} nasıl yapılır?",
    "{item} hakkında nereden detaylı bilgi alabilirim?",
    "{item} ne zaman tarafıma ulaştırılır acaba?",
    "{places} {action} yaparken neden hata alıyorum?",
    "{item} teslimatı için ek bir ücret ödemem gerekiyor mu?",
    "{action} süreci ortalama kaç iş günü sürüyor?",
    "{item} durumunu {places} nereden kontrol edebilirim?",
    "{action} talebimi iptal etmem mümkün mü?",
    "{item} için taksit imkânı bulunuyor mu?",
    "{places} işlem yapabilmek için hangi belgeler gerekli?",
    "{item} ile ilgili müşteri hizmetlerine doğrudan nasıl bağlanabilirim?",
    "{action} için mesai saatleri dışında da destek veriyor musunuz?",
    "{item} başvurum hangi aşamada, öğrenebilir miyim?",
    "{places} yapılan kesintinin gerekçesini açıklar mısınız?",
    "{item} için garanti süresi ne zaman sona eriyor?",
    "{action} işlemi için onay SMS'i ne zaman gelir?",
    "{item} iadesinde kargo ücretini kim karşılıyor?",
    "{places} yeni bir hesap açmak için yaş sınırı var mı?",
    "{item} satın alırken puanlarımı kullanabilir miyim?",
    "{action} yapabilmek için sistemde kayıtlı e-postamı nasıl güncellerim?",
    # Polite indirect inquiry questions
    "{item} hakkında yetkili birinden bilgi almam mümkün müdür?",
    "{action} şartları ve koşulları hakkında aydınlatabilir misiniz?",
    "{places} karşılaştığım bu durum normal bir prosedür müdür?",
    "{item} yenileme işlemi için son tarih nedir acaba?",
    "{action} için sistem üzerinden randevu almam zorunlu mu?",
    "{item} kapsamı dışındaki durumlar nelerdir?",
    "{places} şifremi unuttuğumda yeni aktivasyon kodunu nereden talep edebilirim?",
    "{item} sözleşmesini feshetmek istediğimde ceza bedeli çıkar mı?",
    "{action} sonrası tarafıma onay belgesi veya e-posta gönderilecek mi?",
    "{item} teslimat adresini sonradan değiştirme şansım var mı?",
    # Inverted and colloquial question forms
    "Acaba {item} ne zaman aktif hale gelir?",
    "Peki {action} için hafta sonu hizmet veriliyor mu?",
    "Bu {item} için geçerli olan son kampanya ne zamana kadar sürecek?",
    "Ben {places} {action} yapamıyorum, sistemde bir sorun mu var?",
    "Neden {item} için herhangi bir bilgilendirme mesajı gelmedi?",
    "Hangi durumlarda {item} için para iadesi talep edebiliyorum?",
    "Mobil cihazımdan {action} yapabilmem için ayrı bir ayar gerekiyor mu?",
    "Öğrenmek istediğim konu şu: {item} için değişim hakkım saklı mı?",
    "{item} neden hala onaylanmadı, sebebi nedir?",
    "{action} yaparken kimlik doğrulaması şart mı acaba?"
]

# For Şikâyet (Complaint)
COMPLAINT_TEMPLATES = [
    # Dissatisfaction & failure
    "{item} günlerdir elime ulaşmadı, mağdur edildim.",
    "{places} {action} yaparken sistem sürekli çöküyor ve işlem başarısız oluyor.",
    "Böyle bir ilgisizlik ve sorumsuzluk hayatımda görmedim, {item} paramparça geldi.",
    "{item} için defalarca talep açmama rağmen hiç kimse geri dönüş yapmadı.",
    "{action} yapıldı denmesine rağmen hesabımdan haksız yere iki kez para kesilmiş.",
    "{places} görevli personel son derece kaba ve tersleyici davrandı.",
    "{item} bozuk ve kusurlu çıktı, muhatap bulamıyorum.",
    "Kaç gündür bekliyorum, {item} ile ilgili verilen sözlerin hiçbiri tutulmadı.",
    "Sürekli oyalıyorsunuz, {action} için 1 haftadır tek bir adım atılmadı.",
    "{item} kalitesi vadedilenin çok altında, tam bir hayal kırıklığı.",
    "{places} işlem yapmaya çalıştığımda ekran donuyor ve param bloke kalıyor.",
    "{item} teslimatı haber verilmeden ertelenmiş, rezalet bir durum.",
    "Müşteri temsilciniz telefonu yüzüme kapattı, bu saygısızlığı kabul etmiyorum.",
    "{action} ücreti adı altında benden habersiz kesinti yapılmış, derhal iadesini istiyorum.",
    "{item} yanlış gönderilmiş ve iade talebime de ret cevabı verildi, kabul edilemez.",
    "{places} yarım saattir sıra bekliyorum, tek bir gişe bile doğru düzgün çalışmıyor.",
    "Hem {item} teslim edilmedi hem de sistemde teslim edildi görünüyor, bu ne saçmalık!",
    "{action} için çağrı merkezini aradığımda 45 dakika hatta bekletilip hattan düşürüldüm.",
    "{item} vaat edilen tarihten 10 gün sonra geldi, üstelik hasarlıydı.",
    "Verdiğiniz hizmet kalitesi sıfır, {item} sorununu çözmezseniz yasal haklarımı kullanacağım.",
    # Strong complaints & frustration
    "İki haftadır {item} bekliyorum, hiçbir açıklama yapılmıyor, yazıklar olsun.",
    "{places} personelin ilgisizliği yüzünden {action} işlemimi tamamlayamadım ve ceza yedim.",
    "Parasını peşin ödediğim {item} hala kargoya dahi verilmedi, derhal iptal edin.",
    "{action} sırasında alınan komisyon oranları tamamen fahiş, soygun resmen.",
    "Yenilediğim {item} eskisinden daha kötü çalışıyor, resmen kandırıldık.",
    "{places} hijyen ve düzen namına hiçbir şey yok, tam anlamıyla rezillik.",
    "{item} arızalandı ve teknik servis garanti kapsamında olmasına rağmen fahiş ücret talep etti.",
    "Her seferinde aynı mazeretler, {action} sorununa kalıcı bir çözüm üretmekten acizsiniz.",
    "Uygulamanızdaki son güncellemeden sonra {item} tamamen kullanılamaz hale geldi.",
    "{item} için verdiğiniz taahhütlerin arkasında durmuyorsunuz, derhal şikayetçiyim.",
    "Haftalardır oyaladığınız yetmedi, şimdi de {action} için ek evrak istiyorsunuz, pes doğrusu.",
    "{places} yaşadığım bu mağduriyetin telafi edilmesini talep ediyorum.",
    "{item} eksik parçayla teslim edildi ve eksik parça için benden ekstra para istiyorlar.",
    "Cevap veren yok, çözüm sunan yok, {item} konusunda tam bir fiyasko yaşıyoruz.",
    "Paramla rezil oldum, {action} sürecindeki beceriksizliğiniz yüzünden tüm planlarım altüst oldu."
]

# For Öneri (Suggestion)
SUGGESTION_TEMPLATES = [
    # Constructive suggestions & feature requests
    "{item} için mobil uygulamaya canlı takip ve anlık bildirim özelliği eklenmeli.",
    "{action} adımları çok karmaşık, kullanıcı arayüzü daha sade ve anlaşılır hale getirilebilir.",
    "{places} bekleme süresini azaltmak için otomatik hızlı işlem kioskları konulmasını öneriyorum.",
    "{item} teslimatında çevre dostu geri dönüştürülebilir ambalaj kullanılsa çok daha iyi olur.",
    "{action} işlemini tamamlayan kullanıcılara sadakat puanı veya indirim tanımlanması faydalı olacaktır.",
    "{item} seçeneklerine gece modu ve görme engelliler için sesli asistan desteği getirilmeli.",
    "{places} mesai saatlerinin akşam 20:00'ye kadar uzatılması çalışanlar için büyük kolaylık sağlar.",
    "{item} iadelerinde kuryenin adresten ücretsiz teslim alması gibi bir alternatif sunulabilir.",
    "{action} sürecinde kullanıcılara adım adım SMS ve e-posta bilgilendirmesi yapılması güveni artırır.",
    "{item} için taksit seçeneklerinin artırılması öğrenci ve dar gelirli kullanıcıları rahatlatacaktır.",
    "Uygulamaya arama filtresi ve detaylı sıralama kriterleri eklenirse aradığımızı çok daha rahat buluruz.",
    "{item} kullanım kılavuzunun video formatında karekod ile ürün üzerine basılmasını tavsiye ederim.",
    "{places} hafta sonları da nöbetçi destek ekibi bulundurulması hizmet kalitesini ciddi oranda yükseltir.",
    "{action} ekranında sık sorulan sorular ve canlı destek butonu yan yana konumlandırılabilir.",
    "{item} paketinde yedek parça ve montaj aparatlarının da standart olarak sunulması çok yerinde bir karar olur.",
    "{action} formunun tek sayfaya indirilip gereksiz onay kutularının kaldırılmasını öneririm.",
    "{item} için toplu alımlarda kademeli indirim baremleri uygulanırsa kurumsal müşteriler için çok cazip olur.",
    "{places} müşteri memnuniyet anketlerinin tek tıkla oylanabileceği pratik bir arayüz geliştirilebilir.",
    "{item} aboneliğinde kullanılmayan hakların bir sonraki aya devretmesi seçeneği getirilmelidir.",
    "{action} için onay mekanizmasında parmak izi veya biyometrik giriş seçeneği sunulursa güvenlik artar.",
    # Advice & enhancements
    "Bence {item} için kişiselleştirilebilir profil temaları ve bildirim tercihleri eklenmeli.",
    "Tavsiyem, {places} yoğun saatlerde yoğunluk grafiği gösterilerek kullanıcıların yönlendirilmesidir.",
    "{action} sonrasında kullanıcının geri bildirim bırakabileceği hızlı bir değerlendirme butonu konulmalı.",
    "{item} tasarımında ergonomik iyileştirmeler yapılırsa uzun süreli kullanımlarda çok daha konforlu olur.",
    "{places} rezervasyon sistemi üzerinden önceden sıra numarası alma özelliği entegre edilebilir.",
    "{item} ile ilgili teknik destek taleplerinde ekran kaydı yükleme imkânı sağlanması çözümü hızlandırır.",
    "{action} iptal sürecinde para iadesinin aynı gün karta yansıtılması yönünde altyapı iyileştirmesi yapılabilir.",
    "{item} için sık güncellenen bir şeffaflık ve güncelleme günlüğü (changelog) yayınlanması güzel olur.",
    "Mobil cihazlarda {places} gezinirken çökme olmaması için bellek optimizasyonu yapılması gerekiyor.",
    "{item} kategorisinde filtreleme yaparken fiyat aralığı ve kullanıcı puanı filtresi birlikte seçilebilmeli."
]

def generate_domain_examples(domain_key, domain_data):
    items = domain_data["items"]
    actions = domain_data["actions"]
    places = domain_data["places"]
    
    examples = []
    
    # Generate Soru
    for tmpl in QUESTION_TEMPLATES:
        for _ in range(2):
            item = random.choice(items)
            action = random.choice(actions)
            place = random.choice(places)
            text = tmpl.format(item=item, action=action, places=place)
            examples.append({"text": text, "label": "Soru", "domain": domain_key})
            
    # Generate Şikâyet
    for tmpl in COMPLAINT_TEMPLATES:
        for _ in range(2):
            item = random.choice(items)
            action = random.choice(actions)
            place = random.choice(places)
            text = tmpl.format(item=item, action=action, places=place)
            examples.append({"text": text, "label": "Şikâyet", "domain": domain_key})
            
    # Generate Öneri
    for tmpl in SUGGESTION_TEMPLATES:
        for _ in range(2):
            item = random.choice(items)
            action = random.choice(actions)
            place = random.choice(places)
            text = tmpl.format(item=item, action=action, places=place)
            examples.append({"text": text, "label": "Öneri", "domain": domain_key})
            
    return examples

# Additional hand-crafted natural Turkish edge-cases, idioms, and conversational sentences
CURATED_EXAMPLES = [
    # Soru
    {"text": "Bu ürünün başka renk veya beden seçenekleri de gelecek mi acaba?", "label": "Soru", "domain": "eticaret"},
    {"text": "Yurtdışı kullanımında roaming ücreti günlük mü yoksa aylık mı yansıtılıyor?", "label": "Soru", "domain": "telekom"},
    {"text": "Öğrenci indiriminden yararlanmak için e-Devlet belgesi yeterli oluyor mu?", "label": "Soru", "domain": "egitim"},
    {"text": "İnternet bankacılığı şifremi bloke ettim, şubeye gitmeden nasıl açtırabilirim?", "label": "Soru", "domain": "banka"},
    {"text": "Kan tahlili sonuçlarım e-Nabız sistemine ne zaman düşer?", "label": "Soru", "domain": "saglik"},
    {"text": "Otobüs seferlerinde evcil hayvan taşıma kuralları ve kafes ölçüleri nelerdir?", "label": "Soru", "domain": "ulasim"},
    {"text": "Kargom şu an dağıtım şubesinde görünüyor, gidip kendim elden alabilir miyim?", "label": "Soru", "domain": "kargo"},
    {"text": "Sipariş ettiğim menüye acı sos ve ekstra peynir ekleme şansımız var mı?", "label": "Soru", "domain": "restoran"},
    {"text": "Belediye yüzme havuzu kayıtları hangi tarihler arasında alınıyor?", "label": "Soru", "domain": "belediye"},
    {"text": "Yıllık üyelik planına geçersem geriye kalan ayların farkı iade edilir mi?", "label": "Soru", "domain": "yazilim"},
    {"text": "Garanti belgesini kaybettim, faturanın çıktısı teknik servis için geçerli midir?", "label": "Soru", "domain": "eticaret"},
    {"text": "Sistem üzerinden adres değişikliği yaptım, önceki siparişlerimi etkiler mi?", "label": "Soru", "domain": "eticaret"},
    {"text": "Kartımın temassız ödeme limitini mobil uygulamadan kendim belirleyebilir miyim?", "label": "Soru", "domain": "banka"},
    {"text": "Ders çakışması durumunda dilekçeyi kime ve hangi tarihe kadar teslim etmeliyiz?", "label": "Soru", "domain": "egitim"},
    {"text": "Ev interneti için taahhüt bitimine ne kadar kaldığını nereden görebilirim?", "label": "Soru", "domain": "telekom"},

    # Şikâyet
    {"text": "Ürünün kutusu paramparça ve ezik geldi, kargo firması kesinlikle özen göstermemiş.", "label": "Şikâyet", "domain": "kargo"},
    {"text": "Saatlerdir arıyorum fakat hiçbir yetkili telefona bakmıyor, böyle sorumsuzluk olmaz.", "label": "Şikâyet", "domain": "telekom"},
    {"text": "Hesabımdan haberim olmadan iki kez yıllık kart aidatı çekilmiş, derhal iade edilmeli.", "label": "Şikâyet", "domain": "banka"},
    {"text": "Randevu saatimden 1.5 saat geçmesine rağmen hala muayeneye alınmadım, içeride kimse yok.", "label": "Şikâyet", "domain": "saglik"},
    {"text": "Yemek tamamen buz gibi geldi, paketin içine çorba dökülmüş ve ekmekler ıslanmış.", "label": "Şikâyet", "domain": "restoran"},
    {"text": "Otobüs 40 dakika rötarlı kalktı ve klimalar çalışmıyordu, yolculuk eziyete dönüştü.", "label": "Şikâyet", "domain": "ulasim"},
    {"text": "Son güncellemeden sonra telefon donuyor, uygulama kendi kendine kapanıp duruyor.", "label": "Şikâyet", "domain": "yazilim"},
    {"text": "Sokağımızdaki çöpler üç gündür toplanmıyor, çevreye berbat bir koku yayılıyor.", "label": "Şikâyet", "domain": "belediye"},
    {"text": "İade ettiğim montun parası 25 gündür banka hesabıma yatırılmadı, sürekli oyalıyorlar.", "label": "Şikâyet", "domain": "eticaret"},
    {"text": "Sınav notları haftalar geçmesine rağmen sisteme girilmedi, mağdur ediliyoruz.", "label": "Şikâyet", "domain": "egitim"},
    {"text": "Defalarca arıza kaydı bıraktım ama internet hızım hala vaat edilenin onda biri bile değil.", "label": "Şikâyet", "domain": "telekom"},
    {"text": "Sipariş ettiğim ayakkabının biri 42 diğeri 43 numara çıktı, kontrol etmeden nasıl yolluyorsunuz?", "label": "Şikâyet", "domain": "eticaret"},
    {"text": "Kasiyerin kaba tavırları ve saygısızca cevap vermesi kabul edilebilir gibi değil.", "label": "Şikâyet", "domain": "eticaret"},
    {"text": "Banka ATM'si paramı yuttu ve müşteri hizmetleri 15 gün içinde anca incelenir diyor.", "label": "Şikâyet", "domain": "banka"},
    {"text": "Uçak bagajımı kaybetti ve yetkililer konuyla ilgili hiçbir açıklama yapmıyor.", "label": "Şikâyet", "domain": "ulasim"},

    # Öneri
    {"text": "Mobil uygulamaya koyu tema (karanlık mod) seçeneği eklenirse göz yorgunluğunu çok azaltır.", "label": "Öneri", "domain": "yazilim"},
    {"text": "Sık sipariş veren daimi müşteriler için kargo bedava aboneliği getirilmesini tavsiye ederim.", "label": "Öneri", "domain": "eticaret"},
    {"text": "Otobüs duraklarına akıllı dijital ekranlar konulsa ve gelen aracın dakikası yazsa harika olur.", "label": "Öneri", "domain": "belediye"},
    {"text": "Kart harcamalarını harcama türüne göre grafiklerle özetleyen bir bütçe sekmesi açılabilir.", "label": "Öneri", "domain": "banka"},
    {"text": "Restoranda menülerin yanına kalori ve alerjen uyarılarının yazılması sağlık açısından çok faydalı olur.", "label": "Öneri", "domain": "restoran"},
    {"text": "Kütüphanede çalışma salonlarına priz sayısı artırılmalı ve sessiz çalışma kabinleri yapılmalı.", "label": "Öneri", "domain": "egitim"},
    {"text": "Kargolarda teslimat öncesi kuryenin konumu canlı harita üzerinden takip edilebilmeli.", "label": "Öneri", "domain": "kargo"},
    {"text": "Tahlil sonuçları çıktığında hastaya doğrudan otomatik SMS bildirimi gönderilmesi çok pratik olur.", "label": "Öneri", "domain": "saglik"},
    {"text": "Uçuşlarda koltuk arkası ekran yerine yolcuların kendi telefonundan bağlanabileceği Wi-Fi ağı kurulabilir.", "label": "Öneri", "domain": "ulasim"},
    {"text": "Fatura tutarı belirlenen üst limiti aştığında otomatik uyarı SMS'i atılması sürpriz faturaları önler.", "label": "Öneri", "domain": "telekom"},
    {"text": "Geri dönüştürülebilir bez torbaların kargo ambalajı olarak kullanılması doğaya büyük katkı sağlar.", "label": "Öneri", "domain": "eticaret"},
    {"text": "Sık sorulan sorular kısmına video anlatımlı kısa rehberler eklenirse çağrı merkezi yükü hafifler.", "label": "Öneri", "domain": "yazilim"},
    {"text": "Mahalle aralarındaki kaldırımlara bebek arabası ve tekerlekli sandalyeler için rampa yapılmalı.", "label": "Öneri", "domain": "belediye"},
    {"text": "Mobil şubeden vadeli hesap açarken faiz oranlarını karşılaştırmalı gösteren bir simülatör eklense iyi olur.", "label": "Öneri", "domain": "banka"},
    {"text": "Öğrenci işleri evrak onay sürecini tamamen dijital imzalı hale getirirse kuyruklar sona erer.", "label": "Öneri", "domain": "egitim"}
]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_dataset():
    all_records = []
    
    # 1. Generate from all 10 domains
    for d_key, d_data in DOMAINS.items():
        domain_records = generate_domain_examples(d_key, d_data)
        all_records.extend(domain_records)
        
    # 2. Add curated edge cases
    all_records.extend(CURATED_EXAMPLES)
    
    # 3. Deduplicate
    seen_texts = set()
    unique_records = []
    for r in all_records:
        cleaned = clean_text(r["text"])
        norm = cleaned.lower().replace("ı", "i").replace("ç", "c").replace("ş", "s").replace("ğ", "g").replace("ü", "u").replace("ö", "o")
        norm = re.sub(r'[^\w\s]', '', norm)
        if norm not in seen_texts:
            seen_texts.add(norm)
            unique_records.append({
                "text": cleaned,
                "label": r["label"],
                "domain": r["domain"]
            })
            
    df = pd.DataFrame(unique_records)
    
    # Shuffle
    df = df.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)
    
    print(f"Total Unique Samples Generated: {len(df)}")
    print("\nClass Distribution:")
    print(df["label"].value_counts())
    print("\nDomain Distribution:")
    print(df["domain"].value_counts())
    
    # Stratified Split (80% Train, 20% Test)
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=df["label"]
    )
    
    # Verify no leakage
    train_texts = set(train_df["text"])
    test_texts = set(test_df["text"])
    leakage = train_texts.intersection(test_texts)
    assert len(leakage) == 0, f"Data leakage detected! {len(leakage)} overlapping samples."
    print("\n[VERIFIED] Zero data leakage between train and test sets.")
    
    # Save files
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/turkish_text_dataset.csv", index=False, encoding="utf-8")
    df.to_json("data/turkish_text_dataset.jsonl", orient="records", lines=True, force_ascii=False)
    
    train_df.to_csv("data/train.csv", index=False, encoding="utf-8")
    test_df.to_csv("data/test.csv", index=False, encoding="utf-8")
    
    print(f"\nTrain set: {len(train_df)} samples")
    print("Train label distribution:")
    print(train_df["label"].value_counts())
    print(f"\nTest set: {len(test_df)} samples")
    print("Test label distribution:")
    print(test_df["label"].value_counts())
    print("\nDataset generation completed successfully.")

if __name__ == "__main__":
    build_dataset()

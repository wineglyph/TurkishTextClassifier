# Error Analysis — TurkishTextClassifier Synthetic Evaluation

**83 of 450 examples were misclassified.** Every incorrect prediction is listed below with the source sentence, gold label, predicted label, production confidence, and a text-based hypothesis for the error. The reasons are diagnostic hypotheses based on linguistic cues, not claims about internal model reasoning.

## Error pattern summary

| Gold label | Predicted label | Count |
|---|---|---:|
| Şikâyet | Soru | 19 |
| Şikâyet | Öneri | 16 |
| Öneri | Soru | 10 |
| Öneri | Şikâyet | 38 |

### Main recurring patterns

- **Öneri → Şikâyet (38 cases):** short imperative requests, feature ideas without an explicit “öneriyorum/öneri” marker, and words associated with service problems (for example, delay, cancellation, queue, invoice, or breakdown) are frequent.
- **Öneri → Soru (10 cases):** indirect/hedged suggestion language (“olabilir”, “yararlı olabilir”, “gösterebilir”) and feature requests expressed as information/visibility needs appear to be confused with questions.
- **Şikâyet → Soru (19 cases):** many complaints are neutral declarative incident reports without an explicit emotion, remedy request, or question-free complaint marker; procedural terms such as appointment, payment, refund, and delivery may resemble information inquiries.
- **Şikâyet → Öneri (16 cases):** feature/technical vocabulary or a possible solution in the complaint text may outweigh the negative experience; some examples are short or use nonstandard spelling.
- **Soru:** all 150 gold Soru items were classified correctly in this dataset, although some non-question examples were also predicted as Soru (precision is therefore below 1.0).

## All misclassified examples

### Gold label: Şikâyet (35 errors)

#### SYN-0023 — Şikâyet → Öneri

- **Confidence:** 0.3740
- **Sentence:** “Ürün açıklamasındaki ölçülerle gelen ürünün ölçüleri birbirini tutmuyor.”
- **Likely reason:** Ölçü uyuşmazlığı açık bir olumsuz deneyim olsa da cümle nötr bir tespit biçiminde; memnuniyetsizlik veya çözüm talebi belirgin değil.

#### SYN-0027 — Şikâyet → Öneri

- **Confidence:** 0.4349
- **Sentence:** “Satıcıyla iletişim kurulamıyor, platform da hatalı ilanı kaldırmak için hiçbir adım atmıyor.”
- **Likely reason:** Satıcı/platform/ilan kelimeleri ve “adım atmıyor” ifadesi şikâyeti destekliyor; ancak olay anlatımı, öneri/ürün yönetimi metinleriyle sözcüksel olarak örtüşmüş olabilir.

#### SYN-0063 — Şikâyet → Soru

- **Confidence:** 0.3807
- **Sentence:** “Kredi kartı ekstreme açıklamasız bir sigorta bedeli eklenmiş, iptal başvurumu da sonuçlandırmıyorsunuz.”
- **Likely reason:** Açıklamasız ücret ve sonuçlanmayan iptal başvurusu şikâyet; ancak finansal işlem/ücret açıklaması bağlamı soru örnekleriyle de güçlü biçimde örtüşüyor.

#### SYN-0065 — Şikâyet → Soru

- **Confidence:** 0.4556
- **Sentence:** “Yurt dışındaki hesaba gönderdiğim tutar, alıcı bankanın açıklanmayan masrafları nedeniyle eksik ulaşmış; dekontta kesintinin kaynağı görünmüyor.”
- **Likely reason:** Eksik ulaşan transfer şikâyeti nötr bir olay raporu olarak yazılmış; açık öfke, talep veya “şikâyetçiyim” gibi belirteçler bulunmuyor.

#### SYN-0068 — Şikâyet → Öneri

- **Confidence:** 0.4019
- **Sentence:** “Mobil uygulama gün boyu açılmadığı için kendi paramı kullanamadım.”
- **Likely reason:** Uygulamanın açılmaması ve paraya erişememe açık bir aksaklık; model bunu uygulamaya erişim/işlev geliştirme bağlamıyla karıştırmış olabilir.

#### SYN-0073 — Şikâyet → Soru

- **Confidence:** 0.4092
- **Sentence:** “hesabimdan onayim olmadan para cikmis, itiraz formunu da sistem hata vererek gondermiyor.”
- **Likely reason:** Türkçe karakterleri atlanmış yazım, “hesap/para/itiraz formu” gibi finansal terimlerin temsilini zayıflatmış olabilir; şikâyet doğrudan bir soru cümlesiyle de ifade edilmiyor.

#### SYN-0110 — Şikâyet → Soru

- **Confidence:** 0.5273
- **Sentence:** “Kurulum ekibi belirtilen saatte gelmedi, yeni randevu için de günler sonrasına tarih verildi.”
- **Likely reason:** Kurulum ekibinin gelmemesi şikâyet; randevuya yeniden tarih verilmesi ise planlama/işlem bilgisi talebi gibi algılanmış olabilir.

#### SYN-0115 — Şikâyet → Öneri

- **Confidence:** 0.3668
- **Sentence:** “Taahhüt iptali için istenen cayma bedeli açıklanan tutarın çok üzerinde çıktı; hesaplamayı paylaşmıyorsunuz.”
- **Likely reason:** Cayma bedelinin fazla olması şikâyet; son bölümdeki hesaplama açıklaması beklentisi, açıklama talebi veya yeni bir bilgilendirme özelliği gibi yorumlanmış olabilir.

#### SYN-0116 — Şikâyet → Soru

- **Confidence:** 0.5486
- **Sentence:** “Modem değişimi için ücret alındı fakat yeni cihaz da ilk gününden beri bağlantıyı düşürüyor.”
- **Likely reason:** Ücret ödenmesine rağmen modem bağlantısının kopması şikâyet; modem değişimi ve bağlantı terimleri teknik destek/bilgi sorularıyla örtüşmüş olabilir.

#### SYN-0160 — Şikâyet → Öneri

- **Confidence:** 0.5499
- **Sentence:** “Ücretli sürüme geçtim, buna rağmen reklamlar ekrandan kalkmadı ve destek ekibi ödeme kaydını bulamadı.”
- **Likely reason:** Ödeme yapıldığı hâlde reklamların kalkmaması ve destek kaydının bulunamaması belirgin şikâyet; ücretli sürüm/reklam işlevleri ürün özelliği metinleriyle karışmış olabilir.

#### SYN-0162 — Şikâyet → Öneri

- **Confidence:** 0.4524
- **Sentence:** “Güncelleme notlarında belirtilmeyen izinler istendi ve uygulama bunları reddedince çalışmayı durdurdu.”
- **Likely reason:** İzinler ve güncelleme davranışı teknik ürün dili taşıyor; sorun anlatımı bulunmasına rağmen izin yönetimi/uygulama özelliği çağrışımı öneri sınıfına çekmiş olabilir.

#### SYN-0165 — Şikâyet → Öneri

- **Confidence:** 0.5228
- **Sentence:** “yedekleme basarili yazmasina ragmen eski notlarim geri yuklenmedi.”
- **Likely reason:** Türkçe karakterleri atlanmış metinde yedekleme ve geri yükleme terimleri öne çıkıyor. Başarısız geri yükleme, özellik/işlev talebi gibi sınıflandırılmış olabilir.

#### SYN-0200 — Şikâyet → Soru

- **Confidence:** 0.4021
- **Sentence:** “Sefer iptal edildiği hâlde bilet bedelinin iadesi için haftalardır bekletiliyorum.”
- **Likely reason:** İptal sonrası iade gecikmesi şikâyet; bilet bedeli iadesi, kullanıcıların sıkça bilgi istediği bir işlem olduğundan soru örneklerine benzemiş olabilir.

#### SYN-0202 — Şikâyet → Soru

- **Confidence:** 0.4761
- **Sentence:** “Araç zamanında gelmedi.”
- **Likely reason:** Kısa ve nötr olay bildirimi, gecikmenin yol açtığı memnuniyetsizliği veya açık bir talebi belirtmiyor; bu nedenle soru sınıfına kaymış olabilir.

#### SYN-0203 — Şikâyet → Öneri

- **Confidence:** 0.3906
- **Sentence:** “Koltuk numaram başka yolcuya da verilmiş.”
- **Likely reason:** Başka yolcuya da verilen koltuk numarası bir hizmet hatası; ancak tek cümlelik nötr tespit, açık şikâyet dili içermediği için yanlış sınıflandırılmış olabilir.

#### SYN-0204 — Şikâyet → Öneri

- **Confidence:** 0.3859
- **Sentence:** “Durakta sefer bilgisi gösteren ekran kapalı.”
- **Likely reason:** Kapalı sefer bilgi ekranı şikâyet; “durak/sefer bilgisi/ekran” terimleri bir bilgi ekranı özelliği veya geliştirme isteğiyle örtüşmüş olabilir.

#### SYN-0210 — Şikâyet → Öneri

- **Confidence:** 0.3937
- **Sentence:** “sefer iptalini duraga geldigimde ogrendim, baska ulasim bulmak icin uzun sure ugrastim.”
- **Likely reason:** İptalin geç öğrenilmesi olumsuz deneyim; Türkçe karakterleri atlanmış yazım ve çözüm talebi içermeyen olay anlatımı şikâyet sinyalini zayıflatmış olabilir.

#### SYN-0244 — Şikâyet → Soru

- **Confidence:** 0.6425
- **Sentence:** “Randevu onay mesajı gelmediği için muayeneye alınmadım, sistemdeki kayıt hatasının bedelini ben ödedim.”
- **Likely reason:** Randevu onay mesajının gelmemesi şikâyet; cümlede sistem kaydı ve muayeneye kabul edilmeme anlatılıyor, ancak soru/işlem desteği diline benzeyen randevu terimleri ağır basmış olabilir.

#### SYN-0247 — Şikâyet → Soru

- **Confidence:** 0.4815
- **Sentence:** “Telefonla randevu hattına ulaşamıyorum.”
- **Likely reason:** Telefon hattına ulaşılamaması şikâyet; kısa ve doğrudan ifade, ne yaşandığını söylemesine rağmen açık talep veya güçlü duygusal belirteç içermiyor.

#### SYN-0250 — Şikâyet → Soru

- **Confidence:** 0.4153
- **Sentence:** “Tahlil için aç kalmam söylendi ancak laboratuvarın kapalı olduğu son anda bildirildi; bütün sabahım boşa gitti.”
- **Likely reason:** Tahlil hazırlığı ve laboratuvarın kapalı olması olumsuz deneyim; sağlık/işlem terimleri ve kronolojik anlatım, bilgi alma sorularıyla karışmış olabilir.

#### SYN-0252 — Şikâyet → Soru

- **Confidence:** 0.3760
- **Sentence:** “Acil serviste yönlendirme yapılmadığı için yanlış bölümde bekledim, durumum kötüleşti.”
- **Likely reason:** Acil serviste yanlış yönlendirme ciddi şikâyet; fakat “acil servis/bölüm/yönlendirme” gibi kurumsal sağlık terimleri soru/başvuru bilgisi kalıplarıyla benzerlik taşıyor olabilir.

#### SYN-0253 — Şikâyet → Öneri

- **Confidence:** 0.4087
- **Sentence:** “randevu saatim degistirilmis ama bana hic bildirim gelmedi, hastaneye bosuna geldim.”
- **Likely reason:** Türkçe karakterleri eksik yazım ve bildirim gelmemesi/boşa gitme anlatımı şikâyet; randevu değişikliği ve bildirim özellikleri ürün önerisiyle karışmış olabilir.

#### SYN-0287 — Şikâyet → Soru

- **Confidence:** 0.4134
- **Sentence:** “Yol çalışması için kazılan bölüm açık bırakılmış; gece aydınlatma olmadığı için yayalar tehlike yaşıyor.”
- **Likely reason:** Tehlike ve aydınlatma eksikliği belirgin şikâyet; ancak cümle kurumsal bir olay bildirimi şeklinde, kişisel memnuniyetsizlik veya açık başvuru talebi yok.

#### SYN-0294 — Şikâyet → Soru

- **Confidence:** 0.5009
- **Sentence:** “Sokak köpekleri için bırakılan su kapları düzenli temizlenmiyor.”
- **Likely reason:** Düzenli temizlenmeyen su kapları hakkında nötr, kısa tespit var; sorunun kime yöneltildiği veya hangi düzeltmenin beklendiği belirtilmediği için şikâyet sinyali zayıf.

#### SYN-0297 — Şikâyet → Öneri

- **Confidence:** 0.4751
- **Sentence:** “Yağmurda alt geçidi su bastı ve uyarı levhası konmadığı için insanlar mahsur kaldı.”
- **Likely reason:** Su baskını ve uyarı levhası eksikliği şikâyet; “uyarı levhası” ve önlenebilir altyapı ihtiyacı, modelde öneri/iyileştirme çağrışımı yaratmış olabilir.

#### SYN-0299 — Şikâyet → Öneri

- **Confidence:** 0.3703
- **Sentence:** “mahalledeki kaldirim kazisi aylardir kapatilmedi, bebek arabasiyla gecemiyoruz.”
- **Likely reason:** Türkçe karakterleri atlanmış, uzun süreli kaldırım kazısı şikâyeti; kamusal altyapı ve erişilebilirlik dili bir iyileştirme önerisiyle karışmış olabilir.

#### SYN-0331 — Şikâyet → Soru

- **Confidence:** 0.3856
- **Sentence:** “Harç ödemesini yaptım ama öğrenci sisteminde borç göründüğü için ders kaydım tamamlanmıyor.”
- **Likely reason:** Ödeme yapıldığı hâlde borç görünmesi ve kaydın tamamlanmaması şikâyet; harç/borç/ödeme sözcükleri bilgi ve bakiye sorgusu kalıplarıyla örtüşüyor olabilir.

#### SYN-0341 — Şikâyet → Öneri

- **Confidence:** 0.5205
- **Sentence:** “Engelli erişimi için ayrılan asansör kilitliydi ve sınav salonuna ulaşmakta ciddi güçlük yaşadım.”
- **Likely reason:** Asansörün kilitli olması ve erişim güçlüğü şikâyet; engelli erişimi ve asansör konusu, altyapı iyileştirme talebi gibi sınıflandırılmış olabilir.

#### SYN-0343 — Şikâyet → Soru

- **Confidence:** 0.4743
- **Sentence:** “ogrenci bilgi sistemi acilmiyor, kayit yenileme son gunu islem yapamadim.”
- **Likely reason:** Türkçe karakterleri eksik kısa sistem arızası anlatımı, açık bir talep veya duygu içermiyor; öğrenci bilgi sistemi ve kayıt yenileme terimleri soru bağlamına yakın.

#### SYN-0345 — Şikâyet → Soru

- **Confidence:** 0.4711
- **Sentence:** “diploma basvurum eksik belge gerekcesiyle reddedilmis ama hangi belge oldugu yazmiyor.”
- **Likely reason:** Başvurunun reddi şikâyet olsa da hangi belgenin eksik olduğunun belirtilmemesi doğrudan bilgi boşluğu oluşturuyor; bu soru benzeri bölüm baskın gelmiş olabilir.

#### SYN-0378 — Şikâyet → Soru

- **Confidence:** 0.4346
- **Sentence:** “Kurye ağır paketi kapıya çıkarmayı reddedip aşağı inmemi istedi; ücretini eve teslim için ödemiştim.”
- **Likely reason:** Kurye davranışı ve ödenen eve teslim hizmetinin verilmemesi şikâyet; teslimat/ücret ifadesi, hizmet kapsamı hakkında bilgi sorularıyla örtüşüyor olabilir.

#### SYN-0381 — Şikâyet → Soru

- **Confidence:** 0.4475
- **Sentence:** “Teslimat için ek ücret tahsil edildiği hâlde gönderi şubeden alınmak zorunda bırakıldı.”
- **Likely reason:** Ek ücret alınıp şubeden teslim zorunluluğu şikâyet; teslimat bedeli ve şube alma süreci, kargo/ücret sorgusu kalıplarına yakın.

#### SYN-0426 — Şikâyet → Soru

- **Confidence:** 0.6118
- **Sentence:** “Restoranın havalandırması çalışmadığı için içerisi ağır kokuyordu, masamızı değiştirme isteğimiz reddedildi.”
- **Likely reason:** Havalandırma ve masa değişikliği talebinin reddi şikâyet; restoran deneyimi olumsuz olsa da olay anlatımı bilgi/rezervasyon içeriği gibi sınıflandırılmış olabilir.

#### SYN-0428 — Şikâyet → Öneri

- **Confidence:** 0.5202
- **Sentence:** “Masamız rezervasyon saatinde hazır değildi.”
- **Likely reason:** Rezervasyon saatinde masanın hazır olmaması şikâyet; kısa ve nötr anlatımda memnuniyetsizlik ya da telafi talebi yok, rezervasyon/masa terimleri öneriyle karışmış olabilir.

#### SYN-0435 — Şikâyet → Öneri

- **Confidence:** 0.3569
- **Sentence:** “kahvalti alaninda temiz tabak kalmamis, gorevliler uzun sure yenileme yapmadi.”
- **Likely reason:** Türkçe karakterleri atlanmış, temizlik ve personel yenileme gecikmesi şikâyeti; duygu belirteci içermeyen servis tespiti iyileştirme önerisi gibi algılanmış olabilir.

### Gold label: Öneri (48 errors)

#### SYN-0032 — Öneri → Şikâyet

- **Confidence:** 0.5738
- **Sentence:** “İade talebinin her aşamasında tahmini tamamlanma tarihini gösteren bir durum çizelgesi sunulabilir.”
- **Likely reason:** Öneri kipindeki “sunulabilir” yerine “iade talebi” ve süreç takibi sözcükleri baskın gelmiş olabilir.

#### SYN-0033 — Öneri → Soru

- **Confidence:** 0.5388
- **Sentence:** “Tekrar satın alınan ürünler için önceki teslimat adresini seçmeye yarayan bir kısayol alışverişi kolaylaştırır.”
- **Likely reason:** Önceki adresi seçmeye yarayan kısayol bir özellik önerisi; fakat “seçmeye yarayan” açıklaması, açık öneri bildirimi olmadan bilgi/işlem sorusu gibi algılanmış olabilir.

#### SYN-0036 — Öneri → Soru

- **Confidence:** 0.4609
- **Sentence:** “Dijital faturaların e-posta yanında doğrudan muhasebe yazılımına aktarılabilmesi yararlı olabilir.”
- **Likely reason:** “Yararlı olabilir” ile yumuşatılmış öneri, açık tavsiye fiili içermiyor; dijital fatura ve aktarım kavramları soru örnekleriyle örtüşmüş olabilir.

#### SYN-0038 — Öneri → Soru

- **Confidence:** 0.4849
- **Sentence:** “Kargo ücretini ödeme öncesinde daha görünür gösterin.”
- **Likely reason:** Kısa emir biçimi öneri olarak amaçlanmış; kargo ücreti ve ödeme öncesi görünürlük ise ücret bilgisi sorularına benzeyen bir bağlam oluşturuyor.

#### SYN-0042 — Öneri → Soru

- **Confidence:** 0.3499
- **Sentence:** “Küçük satıcıların performansını yalnızca puanla değil, zamanında teslimat oranıyla da göstermeyi değerlendirebilirsiniz.”
- **Likely reason:** “Değerlendirebilirsiniz” dolaylı ve resmî bir öneri kalıbı; açık “öneriyorum” ifadesinin bulunmaması soru sınıfına kaymaya yol açmış olabilir.

#### SYN-0044 — Öneri → Soru

- **Confidence:** 0.4049
- **Sentence:** “mobil sitede filtreler sayfa degisince sifirlaniyor; secimleri koruyan bir ayar eklenmesini oneririm.”
- **Likely reason:** Cümle aynı anda mevcut bir sorunu (filtrelerin sıfırlanması) ve çözüm önerisini içeriyor. Bu iki işlevin birlikte verilmesi baskın niyeti belirsizleştirmiş olabilir.

#### SYN-0078 — Öneri → Şikâyet

- **Confidence:** 0.3796
- **Sentence:** “Düzenli ödemelerin aylık toplamını gösteren bir özet ekranı müşterilerin nakit akışını planlamasına yardımcı olabilir.”
- **Likely reason:** Özet ekranı önerisi dolaylı bir fayda cümlesiyle aktarılmış; “düzenli ödemeler” ve nakit akışı terimleri mevcut ödeme sorunu şablonlarına benzemiş olabilir.

#### SYN-0084 — Öneri → Şikâyet

- **Confidence:** 0.3810
- **Sentence:** “ATM arızalarını harita üzerinde bildiren bir bölüm eklenebilir.”
- **Likely reason:** Yeni bir harita bölümü önerilse de “ATM arızaları” güçlü bir aksaklık/şikâyet sözcüğü; sınıfı belirleyen olumlu ürün fikri yeterince baskın kalmamış olabilir.

#### SYN-0124 — Öneri → Şikâyet

- **Confidence:** 0.4155
- **Sentence:** “Tarife değişikliğini tamamlamadan önce eski ve yeni paketin toplam maliyetini sade bir ekranda karşılaştırabiliriz.”
- **Likely reason:** Karşılaştırma ekranı açık bir iyileştirme önerisi; tarife, paket ve toplam maliyet sözcükleri ücret sorgusu/şikâyeti kalıplarını çağrıştırmış olabilir.

#### SYN-0127 — Öneri → Şikâyet

- **Confidence:** 0.4551
- **Sentence:** “Fatura uyarısını birkaç gün önce gönderin.”
- **Likely reason:** Çok kısa emir cümlesi, önerinin gerekçesini veya tavsiye belirtecini vermiyor; fatura uyarısı ifadesi olumsuz fatura deneyimleriyle eşleşmiş olabilir.

#### SYN-0134 — Öneri → Soru

- **Confidence:** 0.3938
- **Sentence:** “modem arayuzune teknik bilgi bilmeyenler icin kolay kurulum sihirbazi koyulabilir.”
- **Likely reason:** Türkçe karakterleri atlanmış kısa özellik önerisinde “modem arayüzü/kurulum” teknik terimleri baskın; öneri niyetini açıkça işaretleyen standart ifade zayıf kalmış olabilir.

#### SYN-0171 — Öneri → Şikâyet

- **Confidence:** 0.4615
- **Sentence:** “Hata ekranlarında teknik kodun yanında günlük dille yazılmış bir çözüm önerisi de sunmanızı tavsiye ederim.”
- **Likely reason:** Cümle açıkça çözüm sunulmasını tavsiye ediyor; ancak “hata ekranı” ve “teknik kod” olumsuz hata bağlamı, öneri belirteçlerinden daha baskın gelmiş olabilir.

#### SYN-0172 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Menüyü sadeleştirin.”
- **Likely reason:** İki kelimelik emir biçimi bağlam ve gerekçe içermiyor. Model, doğrudan “sadeleştirin” talebini bir memnuniyetsizlik ifadesi gibi yorumlamış olabilir.

#### SYN-0173 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Klavye kısayolları eklenebilir.”
- **Likely reason:** Çok kısa ve bağlamsız “eklenebilir” önerisinde yalnızca özellik adı var; öneri amacı açık olsa da sınıfı ayıracak ek bağlamsal ipucu az.

#### SYN-0179 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “bildirimleri konuya gore ayri ayri acip kapatma imkani eklenmesini oneriyorum.”
- **Likely reason:** Karakterleri eksiltilmiş kısa cümlede bildirimleri yönetme fikri var; fakat ürün bağlamı ve yarar gerekçesi belirtilmiyor, “bildirim” sözcüğü tek başına yeterli ayrım sağlamamış olabilir.

#### SYN-0212 — Öneri → Soru

- **Confidence:** 0.3821
- **Sentence:** “Aktarma süresi kısa olan biletlerde olası gecikme riskini satın alma aşamasında belirten bir uyarı sunmanızı öneriyorum.”
- **Likely reason:** Gecikme riskini önceden bildiren uyarı önerisi; bilet satın alma ve gecikme terimleri bilgi sorgusu örneklerine daha yakın görünmüş olabilir.

#### SYN-0214 — Öneri → Şikâyet

- **Confidence:** 0.6004
- **Sentence:** “Bilet ücretinin yanında bagaj, koltuk seçimi ve hizmet bedellerini tek bir toplam altında daha açık gösterebilirsiniz.”
- **Likely reason:** Ücret kalemlerini tek toplamda gösterme önerisi, ücret şeffaflığı iyileştirmesi; bilet, bagaj ve hizmet bedeli söz varlığı şikâyet sınıfını çağrıştırmış olabilir.

#### SYN-0217 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Duraklara gölgelik ekleyin.”
- **Likely reason:** Kısa emir cümlesi (gölgelik ekleyin) öneri amacını bağlamlandırmıyor; durak altyapısı hakkında bir şikâyet talebi gibi okunmuş olabilir.

#### SYN-0218 — Öneri → Şikâyet

- **Confidence:** 0.3462
- **Sentence:** “Bilet iptal adımını kısaltın.”
- **Likely reason:** İptal adımını kısaltma önerisi çok kısa ve emir kipinde; “iptal” kelimesi olumsuz işlem/şikâyet bağlamıyla karışmış olabilir.

#### SYN-0219 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Araçlarda USB şarj noktası bulunsun.”
- **Likely reason:** USB noktası talebi emir kipinde ve gerekçesiz verilmiş; öneri belirteci yok, ulaşım hizmetinden beklenti bildiren şikâyet cümlelerine benzeyebilir.

#### SYN-0220 — Öneri → Şikâyet

- **Confidence:** 0.4378
- **Sentence:** “Aktarma merkezlerinde yönlendirme tabelalarını renk ve simgelerle standartlaştırırsanız ziyaretçiler daha kolay yol bulur.”
- **Likely reason:** Tabela standardizasyonu fayda odaklı bir öneri; ancak “ziyaretçiler daha kolay yol bulur” gerekçesi ve koşullu yapı açık tavsiye kalıbı kadar belirgin olmayabilir.

#### SYN-0223 — Öneri → Şikâyet

- **Confidence:** 0.4098
- **Sentence:** “sefer gecikmelerinde tahmini varis saatini uygulamada surekli guncelleyin.”
- **Likely reason:** Türkçe karakterleri atlanmış emir cümlesinde “sefer gecikmeleri” güçlü olumsuz hizmet sözcükleri; iyileştirme fiiliyle birlikte kullanılması karışıklık yaratmış olabilir.

#### SYN-0224 — Öneri → Şikâyet

- **Confidence:** 0.5032
- **Sentence:** “duraklarda qr kodla hat ve tarife bilgisi acilan levhalar kullanilabilir.”
- **Likely reason:** QR kodlu levha önerisi, “kullanılabilir” biçiminde dolaylı kurulmuş ve karakterleri eksik yazılmış; QR/hat/tarife terimleri eğitim verisinde daha seyrek olabilir.

#### SYN-0225 — Öneri → Şikâyet

- **Confidence:** 0.4598
- **Sentence:** “bisiklet tasima kapasitesini gosteren bir filtre eklemenizi oneriyorum.”
- **Likely reason:** Öneri niyeti “öneriyorum” ile açık olsa da Türkçe karakterleri eksik kısa metin ve bisiklet kapasitesi/filtre terimleri sözcüksel eşleşmeyi zayıflatmış olabilir.

#### SYN-0257 — Öneri → Şikâyet

- **Confidence:** 0.4653
- **Sentence:** “Randevu öncesi gerekli hazırlıkların bölüm ve işlem türüne göre tek sayfada gösterilmesi hastaların yanlış hazırlık yapmasını önler.”
- **Likely reason:** Tek sayfalık hazırlık bilgisi açık bir hizmet iyileştirmesi; “yanlış hazırlık” ve hasta/işlem terimleri mevcut olumsuz deneyim veya şikâyet içeriği gibi algılanmış olabilir.

#### SYN-0263 — Öneri → Şikâyet

- **Confidence:** 0.3785
- **Sentence:** “Çocuk polikliniğine ayrı sıra açın.”
- **Likely reason:** Ayrı sıra açılması önerisi kısa emir biçiminde; çocuk polikliniği ve sıra ifadeleri sağlık hizmeti yoğunluğu/şikâyet kalıplarına yakın.

#### SYN-0264 — Öneri → Şikâyet

- **Confidence:** 0.6850
- **Sentence:** “Randevu hatırlatmasını iki kez gönderin.”
- **Likely reason:** Hatırlatma sayısını artıran talep çok kısa ve doğrudan; öneri gerekçesi yok, “randevu hatırlatması” mevcut bildirim sorunu gibi yorumlanmış olabilir.

#### SYN-0265 — Öneri → Şikâyet

- **Confidence:** 0.4419
- **Sentence:** “Hastaların farklı kurumlardaki tetkiklerini kendi izinleriyle tek bir sağlık geçmişinde birleştirebilmesi takip kolaylığı sağlar.”
- **Likely reason:** Sağlık kayıtlarını birleştirme önerisi soyut ve uzun; “tetkik/sağlık geçmişi” terimleri ile takip kolaylığı faydası açık bir öneri kalıbına bağlanmamış olabilir.

#### SYN-0266 — Öneri → Şikâyet

- **Confidence:** 0.4894
- **Sentence:** “Hekim görüşmesi sonrasında verilen talimatların sade dilde özetlendiği bir dijital çıktı hazırlanması yanlış anlamaları azaltır.”
- **Likely reason:** Dijital özet önerisi açık bir iyileştirme; “talimatlar/yanlış anlamalar” ifadeleri hata veya olumsuz deneyim çağrışımı yapmış olabilir.

#### SYN-0267 — Öneri → Şikâyet

- **Confidence:** 0.4251
- **Sentence:** “Hastane içinde laboratuvar ve görüntüleme birimlerine erişimi gösteren erişilebilir bir yön bulma haritası geliştirilebilir.”
- **Likely reason:** Erişilebilir hastane haritası bir özellik önerisi; hastane, laboratuvar, görüntüleme ve erişim sözcükleri mevcut hizmet/erişim sorunlarıyla örtüşüyor olabilir.

#### SYN-0304 — Öneri → Şikâyet

- **Confidence:** 0.4568
- **Sentence:** “Yeni ağaç dikilecek bölgeler belirlenirken sakinlerden çevrim içi konum ve tür önerisi alınabilir.”
- **Likely reason:** Ağaç dikiminde sakinlerden görüş alınması dolaylı ve edilgen bir öneri; açık “öneriyorum” ifadesi yok ve konu/konum sözcükleri şikâyet örneklerine benziyor olabilir.

#### SYN-0307 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Çeşme çevresine oturma alanı koyun.”
- **Likely reason:** Çeşme çevresine oturma alanı ekleme talebi kısa emir kipinde; öneri olduğunu açıklayan gerekçe veya tavsiye belirteci bulunmuyor.

#### SYN-0315 — Öneri → Soru

- **Confidence:** 0.4763
- **Sentence:** “belediye uygulamasina basvurumun hangi masada oldugunu gosteren takip ekleyin.”
- **Likely reason:** Başvuru takibi ekleme talebi emir kipinde; “hangi masada olduğunu gösteren takip” bilgi sorgulama niyetine benzediği için Soru olarak algılanmış olabilir.

#### SYN-0346 — Öneri → Şikâyet

- **Confidence:** 0.3680
- **Sentence:** “Ders kayıt ekranına öğrencinin mezuniyet planına göre uygun dersleri önceliklendiren bir öneri bölümü eklenebilir.”
- **Likely reason:** Ders kayıt ekranına öneri alanı ekleme fikri açıkça iyileştirme; ancak “ders kayıt/mezuniyet planı” kurumsal işlem terimleri ve dolaylı kurgu ayırt ediciliği azaltmış olabilir.

#### SYN-0351 — Öneri → Şikâyet

- **Confidence:** 0.4426
- **Sentence:** “Mezuniyet kontrolünü dönem başında otomatik yapan bir uyarı sistemi kurulması son dakika sorunlarını önleyebilir.”
- **Likely reason:** Otomatik mezuniyet kontrolü önerisi; “son dakika sorunları” ifadesi ve uyarı sistemi kavramı mevcut problem/şikâyet örnekleriyle karışmış olabilir.

#### SYN-0354 — Öneri → Şikâyet

- **Confidence:** 0.3421
- **Sentence:** “Yurt çamaşır makinelerini uygulamadan takip edelim.”
- **Likely reason:** Uygulamadan çamaşır makinesi takibi kısa bir emir/ortak eylem talebi; fayda gerekçesi ve açık öneri sözcüğü yok.

#### SYN-0357 — Öneri → Soru

- **Confidence:** 0.4973
- **Sentence:** “Maddi güçlük yaşayan öğrenciler için yemek bursu başvurusunun diğer burslardan bağımsız yapılabilmesi erişimi kolaylaştırır.”
- **Likely reason:** Yemek bursu başvurusunu ayırma önerisi soyut ve koşullu bir fayda cümlesi; burs/başvuru sözcükleri bilgi edinme sorgularıyla örtüşmüş olabilir.

#### SYN-0359 — Öneri → Şikâyet

- **Confidence:** 0.4598
- **Sentence:** “kampus icindeki su sebillerinin yerini gosteren bir harita eklenmesini oneriyorum.”
- **Likely reason:** Türkçe karakterleri atlanmış ve “öneriyorum” da aksansız yazılmış; kampüs/sebil/harita gibi sözcüklerin az temsil edilmesi öneri niyetinin yakalanmasını zorlaştırmış olabilir.

#### SYN-0360 — Öneri → Şikâyet

- **Confidence:** 0.5188
- **Sentence:** “mezunlarin staj ve is ilanlarini paylasabilecegi bir mentorluk alani acilabilir.”
- **Likely reason:** Türkçe karakterleri atlanmış, soyut ve edilgen bir topluluk özelliği önerisi; açık öneri belirteci ve doğrudan emir bulunmuyor, iş/ilan terimleri farklı niyetlerle karışmış olabilir.

#### SYN-0393 — Öneri → Soru

- **Confidence:** 0.3828
- **Sentence:** “Hasarlı gönderi bildirimi sırasında fotoğraf ekleyip tutanak durumunu aynı ekrandan takip etmek mümkün olabilir.”
- **Likely reason:** “Mümkün olabilir” biçimindeki dolaylı öneri, bir özellik talebinden çok yapılabilirlik sorusu gibi algılanabilir; hasarlı gönderi terimi de şikâyet çağrışımı yapıyor.

#### SYN-0399 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Şube çalışma saatlerini haritada gösterin.”
- **Likely reason:** Şube saatlerini haritada gösterme talebi çok kısa emir biçiminde; öneri gerekçesi veya tavsiye sözcüğü bulunmadığı için olumsuz şube deneyimi olarak yorumlanmış olabilir.

#### SYN-0403 — Öneri → Şikâyet

- **Confidence:** 0.3881
- **Sentence:** “takip ekranina paketin tahmini teslimat gununu guven araligiyla ekleyin.”
- **Likely reason:** Türkçe karakterleri atlanmış kısa emir cümlesinde takip/teslimat terimleri baskın; önerinin faydası açıklanmıyor ve “güven aralığı” teknik ifadesi seyrek olabilir.

#### SYN-0404 — Öneri → Şikâyet

- **Confidence:** 0.4598
- **Sentence:** “sube yogunlugunu gosteren bir sistemle insanlar bosuna sira beklemez.”
- **Likely reason:** Türkçe karakterleri atlanmış dolaylı öneri; “boşuna sıra beklemez” ifadesi mevcut hizmet aksaklığına odaklanıyor ve öneri amacı açıkça işaretlenmiyor.

#### SYN-0442 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Masalara priz ekleyin.”
- **Likely reason:** Masalara priz eklenmesi çok kısa emir kipinde; bağlam/gerekçe olmadığı için bir hizmet talebi şikâyet sınıfına kaymış olabilir.

#### SYN-0443 — Öneri → Şikâyet

- **Confidence:** 0.3897
- **Sentence:** “Menü yazılarını büyütün.”
- **Likely reason:** Menü yazılarını büyütme talebi kısa ve doğrudan; açık öneri veya fayda belirtisi yok, restoran/menü terimleri sınıflandırmayı zorlaştırmış olabilir.

#### SYN-0446 — Öneri → Şikâyet

- **Confidence:** 0.4896
- **Sentence:** “Mutfak yoğunluğuna göre gerçekçi teslimat aralığı veren bir sistem kurulması müşterinin beklentisini doğru yönetir.”
- **Likely reason:** Teslimat aralığı gösterme önerisi fayda odaklı; ancak teslimat süresi ve mutfak yoğunluğu gecikme/servis şikâyetleriyle sözcüksel olarak örtüşüyor olabilir.

#### SYN-0448 — Öneri → Şikâyet

- **Confidence:** 0.5589
- **Sentence:** “uygulamaya siparisin tahmini hazir olma suresini gosteren canli bir durum ekleyin.”
- **Likely reason:** Türkçe karakterleri atlanmış emir biçimi ve sipariş hazırlık süresi terimleri, öneri işaretini zayıflatıp gecikme/işlem şikâyeti çağrışımını güçlendirmiş olabilir.

#### SYN-0450 — Öneri → Şikâyet

- **Confidence:** 0.4299
- **Sentence:** “restoranlarda kalan yemekleri guvenli paketle eve goturmek icin standart bir secenek olsun.”
- **Likely reason:** Artan yemeği paketleme seçeneği önerisi; aksansız kısa metin ve açık “öneriyorum” bulunmaması nedeniyle restoran hizmeti hakkındaki bir şikâyet gibi algılanmış olabilir.

## Limitations of this analysis

- Error explanations are qualitative interpretations of the sentence and confusion pattern; they are not causal explanations extracted from the classifier.
- Confidence is the maximum `predict_proba` class probability rounded by the project API. It should not be treated as calibrated certainty.
- The evaluation set is synthetic and deliberately balanced; this error profile is not a direct estimate of production traffic performance.

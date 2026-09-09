# Order and Inventory Service

Mini marketplace uchun buyurtma va ombor servisi.


## Endpointlar

| Method | Path | Nima qiladi |
|---|---|---|
| POST | /auth/register/ | Ro'yxatdan o'tkazadi |
| POST | /auth/login/ | JWT token beradi |
| POST | /auth/token/refresh/ | Tokenni yangilaydi |
| POST | /products | Mahsulot qo'shadi |
| GET | /products/{id} | Mahsulotni ko'rsatadi |
| POST | /orders | Buyurtma yaratadi (Idempotency-Key header shart) |
| GET | /orders/{id} | Buyurtmani ko'rsatadi |
| POST | /orders/{id}/confirm | Buyurtmani tasdiqlaydi |
| POST | /orders/{id}/cancel | Buyurtmani bekor qiladi |

Products va orders'ga har qanday so'rov uchun token kerak — `Authorization: Bearer <access>`.

## Database Schema

Diagramma shu yerda: [dbdiagram.io](https://dbdiagram.io/d/Order-and-inventory-6aa1045aff72c756bc17a2f5).  SQL fayli: [db/schema.sql](db/schema.sql).

## Nega shunday qildim

Django + DRF oldim, chunki qatlamlarga ajratib (handler → service → repository) yozish qulay chiqadi, JWT uchun ham simplejwt  tayyor kutubxona bor

ORM'siz ishladim, hamma joyda oddiy SQL yozdim (`apps/*/repositories.py` fayllarida). Jadvallarni ham migration bilan emas, `db/schema.sql` orqali yaratdim — Postgres birinchi marta ko'tarilganda o'zi ishga tushirib qo'yadi. Django'ning `models.py` fayllari bor, lekin ular hech narsaga query yubormaydi, faqat ko'rinish uchun turibdi.

Concurrency masalasi — 50 ta so'rov bir vaqtda kelsa, stock 10 bo'lsa, aynan 10 tasi o'tishi kerak edi. Buni bitta UPDATE query bilan hal qildim: `UPDATE ... WHERE stock_quantity >= %s`. Bitta query o'zi atomik ishlaydi, ikkita so'rov bir xil qatorni bir vaqtda o'zgartira olmaydi, shuning uchun alohida lock qo'yishning hojati bo'lmadi. Stock yetmasa, query bo'sh qaytadi va 409 qaytaraman.

Idempotency-Key uchun alohida jadval ochdim, faqat "bu key ishlatilganmi" deb tekshirib qo'ymadim — birinchi so'rovning javobini to'liq saqlab qo'yaman. Shunda xuddi shu key bilan yana so'rov kelsa, hech narsa qayta hisoblanmay, saqlangan javob qaytariladi.

Redis'ni order'ni GET qilishda ishlataman — avval keshdan qarayman, topilmasa bazadan olib, keshga yozib qo'yaman. Order statusi o'zgarsa (confirm yoki cancel bo'lsa) kesh o'chirib yuboriladi. Stock'ni esa ataylab keshlamadim — u tez-tez o'zgaradi, keshlab qo'ysam eski ma'lumot chiqib qolishi mumkin edi.

Celery beat har daqiqada ishlab, 15 daqiqadan ortiq to'lanmay turgan buyurtmalarni topib, avtomatik bekor qiladi.

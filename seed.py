# seed.py
# Заповнення бази тестовими оголошеннями для E-state

from app import app, db, Property

def seed_properties():
    with app.app_context():
        count = Property.query.count()
        if count > 0:
            print(f"⚠️ В базі вже є {count} оголошень. Seed не виконано, щоб не дублювати дані.")
            return

        properties = [
            # 1
            dict(
                title="Затишна 1-кімнатна квартира біля метро Лук'янівська",
                city="Київ",
                property_type="flat",
                price=15000,
                description="Світла квартира з сучасним ремонтом, повністю мебльована, поруч метро та супермаркет.",
                image_url="https://images.unsplash.com/photo-1600585154340-355c9cba26cd"
            ),
            # 2
            dict(
                title="Сучасна 2-кімнатна квартира в новобудові на Позняках",
                city="Київ",
                property_type="flat",
                price=22000,
                description="Новий будинок, підземний паркінг, закрита територія, розвинена інфраструктура.",
                image_url="https://images.unsplash.com/photo-1600607687920-4e2a5345c9a5"
            ),
            # 3
            dict(
                title="Трикімнатна квартира біля Оперного театру",
                city="Львів",
                property_type="flat",
                price=18000,
                description="Історичний центр, висока стеля, якісний ремонт у класичному стилі.",
                image_url="https://images.unsplash.com/photo-1505691723518-36a5ac3be353"
            ),
            # 4
            dict(
                title="Квартира-студія в центрі Одеси",
                city="Одеса",
                property_type="flat",
                price=14000,
                description="5 хвилин до Дерибасівської, закритий двір, кондиціонер, інтернет.",
                image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4"
            ),
            # 5
            dict(
                title="Простора квартира біля парку Шевченка",
                city="Харків",
                property_type="flat",
                price=13000,
                description="2 окремі кімнати, поруч парк, тиха та зелена локація.",
                image_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"
            ),
            # 6
            dict(
                title="Двоповерховий будинок під Києвом",
                city="Київ",
                property_type="house",
                price=4800000,
                description="200 м², власна ділянка 8 соток, гараж, камін, тераса.",
                image_url="https://images.unsplash.com/photo-1568605114967-8130f3a36994"
            ),
            # 7
            dict(
                title="Будинок у передмісті Львова з видом на ліс",
                city="Львів",
                property_type="house",
                price=3500000,
                description="Тихе місце, 2 поверхи, газ, електрика, свердловина, камін.",
                image_url="https://images.unsplash.com/photo-1600585154363-67eb9e2e209d"
            ),
            # 8
            dict(
                title="Сучасний котедж в Одесі біля моря",
                city="Одеса",
                property_type="house",
                price=6200000,
                description="Панорамні вікна, басейн, тераса, 10 хвилин до пляжу.",
                image_url="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7"
            ),
            # 9
            dict(
                title="Будинок з садом у Харкові",
                city="Харків",
                property_type="house",
                price=2800000,
                description="150 м², доглянута ділянка, фруктові дерева, сарай, гараж.",
                image_url="https://images.unsplash.com/photo-1599427303058-f04cbcf4756f"
            ),
            # 10
            dict(
                title="Офісне приміщення в бізнес-центрі класу A",
                city="Київ",
                property_type="commercial",
                price=85000,
                description="Опенспейс + переговорна, рецепція, кондиціонування, паркінг.",
                image_url="https://images.unsplash.com/photo-1504384308090-c894fdcc538d"
            ),
            # 11
            dict(
                title="Магазин на жвавій вулиці у Львові",
                city="Львів",
                property_type="commercial",
                price=55000,
                description="Фасадний вхід, великий потік людей, вітрина, складське приміщення.",
                image_url="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4"
            ),
            # 12
            dict(
                title="Кафе біля моря в Одесі",
                city="Одеса",
                property_type="commercial",
                price=60000,
                description="Готовий бізнес, кухня обладнана, літня тераса, поруч пляж.",
                image_url="https://images.unsplash.com/photo-1514933651103-005eec06c04b"
            ),
            # 13
            dict(
                title="Складське приміщення в індустріальній зоні Харкова",
                city="Харків",
                property_type="commercial",
                price=30000,
                description="500 м², високі стелі, під'їзд вантажного транспорту.",
                image_url="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
            ),
            # 14
            dict(
                title="Земельна ділянка 10 соток під забудову",
                city="Київ",
                property_type="land",
                price=1200000,
                description="Приватний сектор, поруч комунікації, зручний заїзд.",
                image_url="https://images.unsplash.com/photo-1518732714860-b62714ce0c59"
            ),
            # 15
            dict(
                title="Ділянка біля лісу під котедж",
                city="Львів",
                property_type="land",
                price=950000,
                description="Гарний краєвид, тихий район, поряд забудова котеджного типу.",
                image_url="https://images.unsplash.com/photo-1600093463592-9f61807aef11"
            ),
            # 16
            dict(
                title="Земля під комерційну забудову",
                city="Харків",
                property_type="land",
                price=2100000,
                description="Поруч траса, перспективна локація для бізнесу.",
                image_url="https://images.unsplash.com/photo-1529516544815-25ef0c4561d9"
            ),
            # 17
            dict(
                title="Сучасний ЖК у Києві, 1-кімнатна квартира",
                city="Київ",
                property_type="new",
                price=19000,
                description="Новобудова, перша здача, закрита територія, охорона, відеонагляд.",
                image_url="https://images.unsplash.com/photo-1512914890250-353c97c9e7e2"
            ),
            # 18
            dict(
                title="Новобудова у Львові, 2-кімнатна з терасою",
                city="Львів",
                property_type="new",
                price=23000,
                description="Панорамні вікна, вид на місто, підземний паркінг.",
                image_url="https://images.unsplash.com/photo-1460317442991-0ec209397118"
            ),
            # 19
            dict(
                title="Квартира в новобудові біля моря, Одеса",
                city="Одеса",
                property_type="new",
                price=21000,
                description="Закритий комплекс, свій дворик, дитячий майданчик.",
                image_url="https://images.unsplash.com/photo-1512914890250-353c97c9e7e2"
            ),
            # 20
            dict(
                title="Сучасний комплекс у Харкові, 1-кімнатна",
                city="Харків",
                property_type="new",
                price=17000,
                description="Новий ЖК, закрита територія, паркінг, розвинена інфраструктура.",
                image_url="https://images.unsplash.com/photo-1523217582562-09d0def993a6"
            ),
        ]

        for data in properties:
            p = Property(**data)
            db.session.add(p)

        db.session.commit()
        print("✅ 20 оголошень успішно додано в базу!")

if __name__ == "__main__":
    seed_properties()

php
<!DOCTYPE html>
<html>
<head>
    <title>Магазин одежды</title>
    <style>
        /* Некоторый CSS-код для оформления */
        body {
            font-family: Arial, sans-serif;
        }

        .product {
            display: inline-block;
            width: 200px;
            margin: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            text-align: center;
        }
        
        .product img {
            width: 150px;
            height: 150px;
            margin-bottom: 10px;
        }
        
        .product .name {
            font-weight: bold;
        }
        
        .product .price {
            color: #888;
        }
        
        .cart {
            margin-top: 20px;
            font-size: 18px;
        }
        
        .cart .item {
            margin-bottom: 10px;
        }
</style>
</head>
<body>
    <h1>Добро пожаловать в магазин одежды</h1>

    <?php
    // Массив товаров
    $products = [
        [
            'name' => 'Футболка',
            'price' => 500,
            'image' => 'tshirt.jpg'
        ],
        [
            'name' => 'Джинсы',
            'price' => 1000,
            'image' => 'j.jpg'
        ],
        [
            'name' => 'Куртка',
            'price' => 2000,
            'image' => 'ja.jpg'
        ]
    ];

    // Проверяем, был ли отправлен запрос на добавление товара в корзину
    if (isset($_POST['product_id'])) {
        $productId = $_POST['product_id'];
        
        // Проверяем, есть ли такой товар в массиве
        if (isset($products[$productId])) {
            $product = $products[$productId];
            
            // Добавляем товар в корзину (например, сохраняем в сессии)
            if (!isset($_SESSION['cart'])) {
                $_SESSION['cart'] = [];
            }
            
            $_SESSION['cart'][] = $product;
            
            echo '<p>Товар "' . $product['name'] . '" добавлен в корзину!</p>';
        }
    }

    // Отображаем товары из массива
    foreach ($products as $productId => $product) {
        echo '<div class="product">';
        echo '<img src="' . $product['image'] . '" alt="' . $product['name'] . '">';
        echo '<p class="name">' . $product['name'] . '</p>';
        echo '<p class="price">' . $product['price'] . ' руб.</p>';
        echo '<form method="post">';
        echo '<input type="hidden" name="product_id" value="' . $productId . '">';
        echo '<button type="submit">Добавить в корзину</button>';
        echo '</form>';
        echo '</div>';
    }
    ?>

    <div class="cart">
        <h2>Корзина</h2>
        <?php
        // Отображаем выбранные товары в корзине
        if (isset($_SESSION['cart'])) {
            foreach ($_SESSION['cart'] as $item) {
                echo '<div class="item">';
                echo '<p class="name">' . $item['name'] . '</p>';
                echo '<p class="price">' . $item['price'] . ' руб.</p>';
                echo '</div>';
            }
        } else {
            echo '<p>Корзина пуста</p>';
        }
        ?>
    </div>
</body>
</html>
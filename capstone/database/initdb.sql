CREATE TABLE products (
    product_id VARCHAR(50) NOT NULL UNIQUE,
    sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    product_url TEXT NOT NULL UNIQUE,
    thumbnail_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (product_id)
);

CREATE TABLE prices (
    price_id BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    current_price NUMERIC(15, 2),
    original_price NUMERIC(15, 2),
    discount_rate NUMERIC(5, 2),
    quantity_sold INT DEFAULT 0,
    rating_average NUMERIC(3, 2),
    review_count INT DEFAULT 0,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE -- Xóa các bản ghi giá nếu sản phẩm bị xóa
);
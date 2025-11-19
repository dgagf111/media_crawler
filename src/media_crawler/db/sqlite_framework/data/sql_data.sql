-- SQLite测试数据
-- 用于测试和演示的示例数据

-- 插入测试用户数据
INSERT OR IGNORE INTO users (name, email, age, phone, address) VALUES 
('张三', 'zhangsan@example.com', 25, '13800138001', '北京市朝阳区'),
('李四', 'lisi@example.com', 30, '13800138002', '上海市浦东新区'),
('王五', 'wangwu@example.com', 35, '13800138003', '广州市天河区'),
('赵六', 'zhaoliu@example.com', 28, '13800138004', '深圳市南山区'),
('钱七', 'qianqi@example.com', 32, '13800138005', '杭州市西湖区');

-- 插入测试产品数据
INSERT OR IGNORE INTO products (name, description, price, category, stock_quantity) VALUES 
('iPhone 14', '苹果最新款智能手机', 5999.00, '电子产品', 100),
('MacBook Pro', '苹果专业笔记本电脑', 12999.00, '电子产品', 50),
('iPad Air', '苹果平板电脑', 3999.00, '电子产品', 80),
('AirPods Pro', '苹果无线耳机', 1999.00, '电子产品', 200),
('Nike Air Max', '耐克运动鞋', 899.00, '服装鞋帽', 150),
('Adidas Ultra Boost', '阿迪达斯跑鞋', 1299.00, '服装鞋帽', 120),
('Coffee Maker', '咖啡机', 299.00, '家用电器', 60),
('Bluetooth Speaker', '蓝牙音箱', 199.00, '家用电器', 180);

-- 插入测试订单数据
INSERT OR IGNORE INTO orders (user_id, total_amount, status, shipping_address) VALUES 
(1, 5999.00, 'delivered', '北京市朝阳区xxx路xxx号'),
(2, 12999.00, 'shipped', '上海市浦东新区xxx路xxx号'),
(3, 3999.00, 'processing', '广州市天河区xxx路xxx号'),
(1, 1999.00, 'pending', '北京市朝阳区xxx路xxx号'),
(4, 899.00, 'delivered', '深圳市南山区xxx路xxx号');

-- 插入测试订单详情数据
INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES 
(1, 1, 1, 5999.00, 5999.00),
(2, 2, 1, 12999.00, 12999.00),
(3, 3, 1, 3999.00, 3999.00),
(4, 4, 1, 1999.00, 1999.00),
(5, 5, 1, 899.00, 899.00);

-- 插入测试日志数据
INSERT OR IGNORE INTO logs (level, message, source, extra_data) VALUES 
('INFO', '系统启动', 'system', '{"version": "1.0.0"}'),
('INFO', '用户登录', 'auth', '{"user_id": 1, "ip": "192.168.1.1"}'),
('WARNING', '库存不足', 'inventory', '{"product_id": 2, "current_stock": 5}'),
('ERROR', '支付失败', 'payment', '{"order_id": 3, "error_code": "INSUFFICIENT_FUNDS"}'),
('DEBUG', '数据库连接建立', 'database', '{"connection_time": "0.002s"}');

-- 插入额外配置数据
INSERT OR IGNORE INTO config (key, value, description) VALUES 
('company_name', '示例公司', '公司名称'),
('contact_email', 'contact@example.com', '联系邮箱'),
('support_phone', '400-123-4567', '客服电话'),
('timezone', 'Asia/Shanghai', '时区设置'),
('language', 'zh-CN', '语言设置');
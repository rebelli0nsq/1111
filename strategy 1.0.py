import random
import numpy as np

# Визначення дій
ACTIONS = ['stay', 'change']

# Ініціалізація Q-таблиці
Q = np.zeros((3, 2))  # Припускаємо три стани: 0 (нічого), 1 (об'єкт), 2 (анти-об'єкт)

# Параметри навчання
alpha = 0.1  # Швидкість навчання
gamma = 0.9   # Дисконтний фактор
epsilon = 1.0  # Параметр епсілон для ε-жадібної політики
epsilon_min = 0.01  # Мінімальне значення епсілон
epsilon_decay = 0.995  # Зменшення епсілон після кожного епізоду

def update_Q_table(state, action, reward, next_state):
    # Оновлення Q-значення за допомогою формули Q-навчання
    best_next_action = np.max(Q[next_state])
    Q[state][action] += alpha * (reward + gamma * best_next_action - Q[state][action])

def strategy2(b=s3.body):
    v = 100
    a = b.angle
    b.velocity = v * np.cos(a), v * np.sin(a)
    x, y = b.position
    R = getDist(x, y, 350, 250)
    
    ellipse(x, y, 200, 200, stroke=Color(0.5))
    line(x, y, x + 100 * np.cos(a + 0.5), y + 100 * np.sin(a + 0.5), stroke=Color(0.5))
    line(x, y, x + 100 * np.cos(a - 0.5), y + 100 * np.sin(a - 0.5), stroke=Color(0.5))

    if canvas.frame % 10 == 0:  # Кожні n кадрів
        inS = inSector(s1.body.position[0], s1.body.position[1], x, y, 100, a)
        inS2 = inSector(S2[0].body.position[0], S2[0].body.position[1], x, y, 100, a)

        # Визначення стану та винагороди
        if inS:
            state = 1  # об'єкт
            reward = 1 if b.action == 0 else -1
        elif inS2:
            state = 2  # анти-об'єкт
            reward = -1 if b.action == 0 else 1
        else:
            state = 0  # нічого
            reward = 0

        # Вибір дії
        if random.random() < epsilon:  # Імовірність епсілон для випадкового вибору
            action = random.choice([0, 1])  # залишити або змінити
        else:
            action = np.argmax(Q[state])  # вибір дії з найбільшим Q-значенням

        # Виконання дії
        if action == 1:  # якщо змінюємо напрямок
            b.angle = 2 * np.pi * random.random()

        # Оновлення Q-таблиці
        next_state = state  # Для простоти, будемо вважати, що стан залишається тим же
        update_Q_table(state, action, reward, next_state)

        # Запобігання виходу за межі кола
        if R > 180:
            b.angle = getAngle(x, y, 350, 250)

    # Зменшення епсілон для наступних епізодів
    global epsilon
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    # Додатково: вивід Q-таблиці для налагодження
    print("Q-таблиця:", Q)


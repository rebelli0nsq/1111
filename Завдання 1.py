import random

actions = ['rock', 'paper', 'scissors']
Q = {'rock': {'rock': 0, 'paper': 0, 'scissors': 0},
     'paper': {'rock': 0, 'paper': 0, 'scissors': 0},
     'scissors': {'rock': 0, 'paper': 0, 'scissors': 0}}

alpha = 0.1  # швидкість навчання
gamma = 0.9  # коефіцієнт дисконтирования
epsilon = 0.1  # ймовірність вибору випадкової дії

def update_Q_table(state, action, reward, next_state):
    # Оновлення Q-таблиці за класичною формулою Q-навчання
    Q[state][action] += alpha * (reward + gamma * max(Q[next_state].values()) - Q[state][action])

def select_action(state):
    # Вибір дії з ε-жадібною стратегією
    if random.uniform(0, 1) < epsilon:
        return random.choice(actions)
    else:
        return max(Q[state], key=Q[state].get)

def learn():
    state = random.choice(actions)
    while True:
        action = select_action(state)
        # Визначаємо нагороду
        if action == state:
            reward = 0.5  # Нічия
        elif (action == 'rock' and state == 'scissors') or \
             (action == 'paper' and state == 'rock') or \
             (action == 'scissors' and state == 'paper'):
            reward = 1.0  # Перемога
        else:
            reward = 0.0  # Поразка

        next_state = action
        update_Q_table(state, action, reward, next_state)
        state = next_state

        # Умови завершення навчання
        if all(value >= 0.9 for value in Q[state].values()):
            break

# Навчання агента
for i in range(10000):
    learn()

# Виведення результатів
print(Q)
print("Найкраща дія для стану 'rock':", max(Q['rock'], key=Q['rock'].get))

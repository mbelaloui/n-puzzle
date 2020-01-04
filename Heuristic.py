class Heuristic:
    def __init__(self, goal, current, size):
        self.goal = goal
        self.current = current
        self.size = size
        # this variable is a list of the functions name
        self.function = {'Euclidean_distance': self.ft_distance_euclide, 'manhattan': self.ft_manhattan, 'conflicts': self.ft_conflict, 'out_of_row_and_column': self.ft_out_of_row_and_column, 'hamming': self.ft_hamming}

    def ft_distance_euclide(self, nbr_index):
        dis = 0
        for key, element in enumerate(self.current):
            if element != 0:
                key_g = self.goal.index(element)
                x_n, y_n = key % self.size, key / self.size
                x_g, y_g = key_g % self.size, key_g / self.size
                dis += ((x_g - x_n) ** 2 + (y_g - y_n) ** 2) ** 0.5
        return dis

    def ft_out_of_row_and_column(self, nbr_index):
        count = 0
        for key, element in enumerate(self.current):
            if element != 0:
                key_g = self.goal.index(element)
                x_n, y_n = key % self.size, key / self.size
                x_g, y_g = key_g % self.size, key_g / self.size
                if x_g != x_n:
                    count += 1
                if y_n != y_g:
                    count += 1
        return count

    def ft_manhattan(self, nbr_index):
        count = 0
        for key, element in enumerate(self.current):
            if element != 0:
                index = self.goal.index(element)
                x_el, y_el = key % self.size, key / self.size
                x_goal, y_goal = index % self.size, index / self.size
                count += abs(x_el - x_goal) + abs(y_goal - y_el)
        return count

    def ft_hamming(self, nbr_index):
        count = 0
        for key, element in enumerate(self.current):
            if element != 0 and element != self.goal[key]:
                count += 1
        return count

    def ft_conflict(self, nbr_index):
        count = 0
        key = 0
        len_current = self.size ** 2
        while key < len_current:
            if self.current[key] == 0:
                key += 1
                continue
            key_g = nbr_index[self.current[key]]
            x_n, y_n = key % self.size, key / self.size
            x_g, y_g = key_g % self.size, key_g / self.size
            if y_g == y_n and x_n != x_g:
                limit_g = (key / self.size) * self.size
                limit_n = self.size * (key / self.size + 1)
                index_1 = key_g - 1
                while index_1 >= limit_g:
                    index_2 = key + 1
                    while index_2 < limit_n:
                        if self.goal[index_1] == self.current[index_2]:
                            count += 2
                            break
                        index_2 += 1
                    index_1 -= 1
            if x_g == x_n and y_n != y_g:
                index_1 = key_g - self.size
                while index_1 >= 0:
                    index_2 = key + self.size
                    while index_2 < len_current:
                        if self.goal[index_1] == self.current[index_2]:
                            count += 2
                            break
                        index_2 += self.size
                    index_1 -= self.size
            key += 1        
            count += abs(x_n - x_g) + abs(y_g - y_n)
        return count
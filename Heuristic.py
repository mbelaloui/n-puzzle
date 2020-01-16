class Heuristic:
    def __init__(self, goal, current, size):
        self.goal = goal
        self.current = current
        self.size = size
        # this variable is a list of the functions name
        self.function = {'Euclidean_distance': self.ft_distance_euclide, 'manhattan': self.ft_manhattan, 'conflicts': self.ft_conflict, 'out_of_row_and_column': self.ft_out_of_row_and_column, 'hamming': self.ft_hamming}

# we use pythagore rule  A^2 + B^2 = c^2
    def ft_distance_euclide(self, nbr_index):
        dis = 0
        for index_e, element in enumerate(self.current):
            if element != 0:
                index_g  = self.goal.index(element)
                x_e, y_e = index_e % self.size, index_e/ self.size
                x_g, y_g = index_g % self.size, index_g / self.size
                dis += ((x_g - x_e) ** 2 + (y_g - y_e) ** 2) ** 0.5
        return dis

# we add 1 if the x_e and x_g are different and do the same withe y coordinates
    def ft_out_of_row_and_column(self, nbr_index):
        count = 0
        for index_e , element in enumerate(self.current):
            if element != 0:
                index_g  = self.goal.index(element)
                x_e, y_e = index_e % self.size, index_e / self.size
                x_g, y_g = index_g % self.size, index_g / self.size
                if x_g != x_e:
                    count += 1
                if y_e != y_g:
                    count += 1
        return count

#d(A,B) = |X_{B}-X_{A}| + |Y_{B}-Y_{A}|   ...
    def ft_manhattan(self, nbr_index):
        count = 0
        for index_e , element in enumerate(self.current):
            if element != 0:
                index_g = self.goal.index(element)
                x_e, y_e = index_e % self.size, index_e / self.size
                x_g, y_g = index_g % self.size, index_g / self.size
                count += abs(x_e - x_g) + abs(y_g - y_e)
        return count


#if an element isn't well placed so + 1
    def ft_hamming(self, nbr_index):
        count = 0
        for index_e , element in enumerate(self.current):
            if element != 0 and element != self.goal[index_e]:
                count += 1
        return count

#this heuristic allows us to choose a state where the element is closer to its right position
    def ft_conflict(self, nbr_index):
        count = 0
        index_e = 0
        len_current = self.size ** 2
        while index_e < len_current:
            if self.current[index_e] == 0:
                index_e += 1
                continue
            index_g  = nbr_index[self.current[index_e]]
            x_e, y_e = index_e % self.size, index_e / self.size
            x_g, y_g = index_g % self.size, index_g / self.size
            if y_g == y_e and x_e != x_g:
                limit_g = (index_e / self.size) * self.size
                limit_e = self.size * (index_e / self.size + 1)
                index_1 = index_g - 1
                while limit_g <= index_1:
                    index_2 = index_e + 1
                    while index_2 < limit_e:
                        if self.goal[index_1] == self.current[index_2]:
                            count += 2
                            break
                        index_2 += 1
                    index_1 -= 1
            if x_g == x_e and y_e != y_g:
                index_1 = index_g - self.size
                while index_1 >= 0:
                    index_2 = index_e + self.size
                    while index_2 < len_current:
                        if self.goal[index_1] == self.current[index_2]:
                            count += 2
                            break
                        index_2 += self.size
                    index_1 -= self.size
            index_e += 1        
            count += abs(x_e - x_g) + abs(y_g - y_e)
        return count
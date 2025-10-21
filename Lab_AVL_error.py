"""Taller de Árboles AVL: Implementación de un árbol AVL (corregido) con inserción, 
eliminación y visualización.
Andrés Sebastián Pinzón Gutiérrez 2221887
"""
import sys


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        # la altura de un nodo hoja es 1
        self.height = 1


def getHeight(node):
    if not node:
        return 0
    return node.height


def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)


def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))


def rotate_right(y):
    """Rotación a la derecha.
    Devuelve la nueva raíz del subárbol tras la rotación.
    """
    x = y.left
    T2 = x.right

    # realizar rotación
    x.right = y
    y.left = T2

    # actualizar alturas
    updateHeight(y)
    updateHeight(x)

    return x


def rotate_left(x):
    """Rotación a la izquierda.
    Devuelve la nueva raíz del subárbol tras la rotación.
    """
    y = x.right
    T2 = y.left

    # realizar rotación
    y.left = x
    x.right = T2

    # actualizar alturas
    updateHeight(x)
    updateHeight(y)

    return y


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # inserción normal en BST
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            # no se permiten duplicados; devolver el nodo existente
            return node

    # actualizar altura y calcular balance
        updateHeight(node)
        balance = getBalance(node)

        # Caso (izquierdo-izquierdo)
        if balance > 1 and getBalance(node.left) >= 0:
            node = rotate_right(node)
        # Caso (izquierdo-derecho)
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            node = rotate_right(node)
        # Caso (derecho-derecho)
        elif balance < -1 and getBalance(node.right) <= 0:
            node = rotate_left(node)
        # Caso (derecho-izquierdo)
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            node = rotate_left(node)

        return node

    def inorder(self):
        """Devuelve una lista en recorrido inorden."""
        res = []
        self._inorder_recursive(self.root, res)
        return res

    def _inorder_recursive(self, node, res):
        if not node:
            return
        self._inorder_recursive(node.left, res)
        res.append(node.value)
        self._inorder_recursive(node.right, res)

    def print_inorder(self):
        print('Inorden:', ' '.join(str(x) for x in self.inorder()))

    def print_tree(self, node=None, level=0, label='Raíz:'):
        """Esta función ahora redirige a la 
        impresión vertical.
        """
        self.print_vertical()
        return

    def print_vertical(self):
        """Imprime el árbol en formato vertical por niveles.

        Esta representación muestra cada nivel en una línea;
        los nodos nulos se representan con espacios 
        para conservar la alineación.
        """
        h = getHeight(self.root)
        if not self.root:
            print('(vacío)')
            return

        # nivel inicial con la raíz
        level = [self.root]
        for i in range(1, h + 1):
            # espacio entre nodos
            gap = ' ' * (2 ** (h - i + 1) - 1)
            line_parts = []
            for node in level:
                if node is None:
                    line_parts.append(' ' * 17)
                else:
                    # mostrar solo la identidad del nodo (valor)
                    part = f"{node.value}"
                    line_parts.append(part.center(17))
            print(gap.join(line_parts).center(120))

            # construir el siguiente nivel
            next_level = []
            for node in level:
                if node is None:
                    next_level.extend([None, None])
                else:
                    next_level.append(node.left)
                    next_level.append(node.right)
            level = next_level

    def print_vertical_detailed(self):
        """Imprime el árbol por niveles mostrando
        valor, altura y factor de balance.
        Formato por nodo: valor(h=X,b=Y)
        """
        h = getHeight(self.root)
        if not self.root:
            print('(vacío)')
            return

        level = [self.root]
        for i in range(1, h + 1):
            gap = ' ' * (2 ** (h - i + 1) - 1)
            line_parts = []
            for node in level:
                if node is None:
                    line_parts.append(' ' * 23)
                else:
                    b = getBalance(node)
                    part = f"{node.value}(h={node.height},b={b})"
                    line_parts.append(part.center(23))
            print(gap.join(line_parts).center(140))

            next_level = []
            for node in level:
                if node is None:
                    next_level.extend([None, None])
                else:
                    next_level.append(node.left)
                    next_level.append(node.right)
            level = next_level

    def get_min_value_node(self, node):
        """Devuelve el nodo con el valor mínimo 
        en el subárbol (el más a la izquierda)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, value):
        """para reflejar la eliminación.
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        """Elimina recursivamente y vuelve a balancear.

        Devuelve la nueva raíz del subárbol después de la eliminación.
        """
        # caso base
        if not node:
            return node

        # buscar como en un BST
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # este es el nodo a eliminar
            # caso con 0 o 1 hijo
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            # caso con 2 hijos: obtener sucesor inorder (mínimo del subárbol derecho)
            temp = self.get_min_value_node(node.right)
            node.value = temp.value
            # eliminar el sucesor
            node.right = self._delete_recursive(node.right, temp.value)

        # si el árbol tuvo sólo un nodo
        if node is None:
            return node

        # actualizar altura y balancear
        updateHeight(node)
        balance = getBalance(node)

        # Izquierdo Izquierdo
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        # Izquierdo Derecho
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Derecho Derecho
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        # Derecho Izquierdo
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node


if __name__ == '__main__':
    avl = AVLTree()
    values_to_insert = [10, 20, 30, 40, 50, 25]

    print("Insertando valores:", values_to_insert)
    for val in values_to_insert:
        avl.insert(val)

    print("\nInorder tras inserciones:")
    avl.print_inorder()
    print('\nÁrbol (representación):')
    # mostrar representación detallada (valor, altura y balance)
    avl.print_vertical_detailed()
    

    # Ejemplo de eliminación: eliminar 50 y mostrar resultado
    eliminar = 50
    print(f"\nEliminando {eliminar}...")
    avl.delete(eliminar)
    print('Inorder tras eliminación:', avl.inorder())
    print('\nÁrbol final (representación):')
    # representación detallada (valor, altura y factor de balance)
    avl.print_vertical_detailed()
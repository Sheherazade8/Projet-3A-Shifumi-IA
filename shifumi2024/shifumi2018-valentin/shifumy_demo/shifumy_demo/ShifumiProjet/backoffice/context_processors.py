from .Models.modele_arbre.Settings import Load_Tree,Model_Tree,Node , History


def categories(request):
    all_categories = Node()

    return {
        'categories': all_categories,
    }

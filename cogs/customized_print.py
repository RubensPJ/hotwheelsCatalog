# My own print
def printit(*args):
    print("|-===================================================-")
    print("|")


    for arg in args:
        if isinstance(arg, list):
            print("| Título: Informações da Lista")
            print(f"| Número de Valores na Lista: {len(arg)}")
            unique_types = set(type(item).__name__ for item in arg)
            # print(f"| Tipos Únicos na Lista: {', '.join(unique_types)}")
            print("| Lista:")
            print("\n".join(f"|  {item}" for item in arg))
        else:
            print(f"| {arg}")
   


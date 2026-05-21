import sys
import users_wrapper as users

def exibir_menu():
    print("\n=== CLI JSONPlaceholder Users ===")
    print("1. Listar usuários")
    print("2. Ver detalhes de um usuário (Read)")
    print("3. Criar usuário (Create)")
    print("4. Atualizar usuário (Update)")
    print("5. Deletar usuário (Delete)")
    print("6. Sair")
    print("=================================")

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\nBuscando usuários...")
            lista = users.list()
            for u in lista:
                print(f"[{u['id']}] {u['name']} - {u['email']}")

        elif opcao == "2":
            user_id = input("Digite o ID do usuário: ").strip()
            u = users.read(user_id)
            if u:
                print(f"\nNome: {u.get('name')}")
                print(f"Username: {u.get('username')}")
                print(f"Email: {u.get('email')}")
                print(f"Telefone: {u.get('phone')}")
                print(f"Website: {u.get('website')}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            print("\n--- Criar Novo Usuário ---")
            name = input("Nome: ")
            username = input("Username: ")
            email = input("Email: ")
            
            dados = {"name": name, "username": username, "email": email}
            novo_usuario = users.create(dados)
            if novo_usuario:
                print(f"\nSucesso! Usuário criado com ID: {novo_usuario['id']}.")
            else:
                print("Erro ao criar usuário.")

        elif opcao == "4":
            user_id = input("Digite o ID do usuário que deseja atualizar: ").strip()
            print("Deixe em branco para manter o valor atual.")
            
            # Buscando dados atuais para mesclar
            atual = users.read(user_id)
            if not atual:
                print("Usuário não encontrado.")
                continue

            name = input(f"Novo Nome ({atual['name']}): ") or atual['name']
            username = input(f"Novo Username ({atual['username']}): ") or atual['username']
            email = input(f"Novo Email ({atual['email']}): ") or atual['email']

            dados = {"name": name, "username": username, "email": email}
            atualizado = users.update(user_id, dados)
            if atualizado:
                print("\nUsuário atualizado com sucesso!")
                print(atualizado)
            else:
                print("Erro ao atualizar usuário.")

        elif opcao == "5":
            user_id = input("Digite o ID do usuário que deseja deletar: ").strip()
            if users.delete(user_id):
                print(f"\nUsuário {user_id} deletado com sucesso (simulado).")
            else:
                print("Erro ao deletar usuário.")

        elif opcao == "6":
            print("Saindo...")
            sys.exit(0)
            
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
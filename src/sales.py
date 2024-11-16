import pandas as pd


def sales():
    try:
        print("Preparando os dados de sales para processamento")
        df_sales = pd.read_csv("../data/sales.csv")
        print(df_sales)
        df_sales_clean = clean_data_sales(df_sales)
        most_selled_product(df_sales_clean)
        most_selled_category(df_sales_clean)
        daily_average_selled_category(df_sales_clean)
        product_selled_equal_or_more_50(df_sales_clean)
        print("")

    except Exception as e:
        print(f"Erro no processamento: {e}")


def clean_data_sales(df_sales):
    print("Realizando limpeza no dataframe de sales")
    print("Removendo as linhas com a data Invalid Date")
    df_sales_filtered = df_sales.loc[df_sales['date'] != 'Invalid Date']

    print("Novo dataframe criado")
    print(df_sales_filtered)

    print("Limpando dados negativos")
    df_sales_filtered.loc[:, 'price'] = abs(df_sales_filtered['price'])
    df_sales_filtered.loc[:, 'quantity'] = abs(df_sales_filtered['quantity'])

    print("Valores negativos tranformados ")
    print(df_sales_filtered['price'])
    print(df_sales_filtered['quantity'])

    print("Removendo o padrão 00:00:00 da data dos pedidos")
    df_sales_filtered.loc[:, 'date'] = df_sales_filtered['date'].str.replace(' 00:00:00', '', regex=False)

    return df_sales_filtered


def most_selled_product(df_sales):
    print("**Verificando produto mais vendido**")

    df_sales_filtered = df_sales.groupby('product').agg({
        'quantity': 'sum',
        'price': 'sum',
    }).reset_index()
    most_selled = df_sales_filtered.loc[df_sales_filtered['quantity'].idxmax()]
    print(f"O produto mais vendido foi: {most_selled['product']} "
          f"com {most_selled['quantity']} itens vendidos. \n")


def most_selled_category(df_sales):
    print("**Verificando categoria mais vendida**")

    df_sales_filtered = df_sales.groupby('category').agg({
        'quantity': 'sum',
        'price': 'sum',
    }).reset_index()

    df_sales_filtered['total_selled'] = df_sales_filtered['quantity'] * df_sales_filtered['price']

    most_selled = df_sales_filtered.loc[df_sales_filtered['total_selled'].idxmax()]
    print(f"A categoria que mais vendeu o foi: {most_selled['category']}"
          f" e teve um retorno de {round(most_selled['total_selled'], 2)}. \n")


def daily_average_selled_category(df_sales):

    print("**Verificando média diaria das categorias**")
    print("Garantindo o formatod o campo de data")
    df_sales = df_sales.copy()  # Garante que `df_sales` é independente
    df_sales.loc[:, 'date'] = pd.to_datetime(df_sales['date'])

    print("Calculando vendas diarias")
    df_sales.loc[:, 'daily_sales'] = df_sales['price'] * df_sales['quantity']

    print("Agrupando e retornando a média por categoria diaria")
    avg_daily_sales = df_sales.groupby(['category', 'date'])['daily_sales'].mean().reset_index()

    print(f"A média diaria: {avg_daily_sales}")


def product_selled_equal_or_more_50(df_sales):
    print("**Verificando produto vendido mais de 100 vezes em um dia**")
    print("Garantindo o formatod o campo de data")
    df_sales = df_sales.copy()  # Garante que `df_sales` é independente
    df_sales.loc[:, 'date'] = pd.to_datetime(df_sales['date'])

    print("agrupando por produto e quantidade")

    daily_sales = df_sales.groupby(['product', 'date'])['quantity'].sum().reset_index()

    filtered_products = daily_sales[daily_sales['quantity'] >= 50]

    print(f"Produtos que venderam mais de 100 em quantidade por dia: {filtered_products}")


if __name__ == "__main__":
    sales()

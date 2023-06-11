def tabela_price(vp, n, i):
    if n == 0:
        return []

    vp_f = float(vp)
    n_f = float(n)
    i_f = float(i)

    z = (1.0 + i_f) ** n_f
    pmt = vp_f / ((z - 1.0) / (z * i_f))

    parcelas = []

    for periodo in range(n):
        juros = vp_f * i_f
        amortizacao = pmt - juros
        vp_f = vp_f - amortizacao

        parcela = {
            "numero": periodo + 1,
            "valorAmortizacao": float(round(amortizacao, 2)),
            "valorJuros": float(round(juros, 2)),
            "valorPrestacao": float(round(pmt, 2)),
        }

        parcelas.append(parcela)

    return parcelas


def tabela_sac(vp, n, i):
    if n == 0:
        return []

    vp_f = float(vp)
    n_f = float(n)
    i_f = float(i)

    amortizacao = vp_f / n_f

    parcelas = []

    for periodo in range(n):
        juros = vp_f * i_f
        pmt = amortizacao + juros
        vp_f = vp_f - amortizacao

        parcela = {
            "numero": periodo + 1,
            "valorAmortizacao": float(round(amortizacao, 2)),
            "valorJuros": float(round(juros, 2)),
            "valorPrestacao": float(round(pmt, 2)),
        }

        parcelas.append(parcela)

    return parcelas

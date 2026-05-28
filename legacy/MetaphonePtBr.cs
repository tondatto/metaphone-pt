//------------------------------------------------------------------------------
// <copyright file="CSSqlClassFile.cs" company="Microsoft">
//     Copyright (c) Microsoft Corporation.  All rights reserved.
// </copyright>
//------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using System.Text;

namespace Metaphone_BR
{
    public class MetaphonePtBr : Metaphone
    {
        public MetaphonePtBr(string text) : base(text)
        {

        }

        protected internal override void Prepare()
        {
            // Essa letras duplicadas são apenas dor de cabeça. Antes de começar, tiramos o excesso.
            // Otto, Rizzo, Millene, Riccardo (é... com dois "c", achei um desses, é mole?) 
            RemoveMultiples(" ", "b", "c", "g", "l", "t", "p", "d", "f", "j", "k", "m", "v", "n", "z");
        }

        protected internal override void Algorithm()
        {
            // Nomes antigos
            Translate("ph", "F"); // Alphonso
            Translate("th", "T"); // Martha

            Translate("lh", "1");
            // Galdêncio ou Gaudêncio? Descartamos como se fosse vogal
            Ignore("(l)" + NON_VOWEL);
            Translate("l", "L");

            Translate("g[eiy]", "J");
            Translate("g[ao]", "G");
            Translate("gu[ei]", "G");
            Translate("g", "G");

            /* C parecia mais simples no começo */

            // O erro de digitação mais comum q existe "cao" = "ção",
            // não faz parte do metaphone, mas...
            Translate("cao", "S");
            // "Belchior" (Belkior, não Belxior) parece ser exceção
            // mas me lembro de "Melchior" em algum lugar, também.
            Translate("l(chior)\\s", "K2");
            Translate("ch", "X");
            Translate("ck", "K"); // Volta e meia tem uma "Jackeline"
            Translate("cq", "K"); // E um ou outro "Jacques" perdido
            Translate("c[eiy]", "S");
            Translate("c[aou]", "K");
            Translate("c", "K");
            Translate("ç", "S");

            Translate("rr", "2");
            Translate("\\s(r)", "2"); // Raul, Régis
            Translate("(r)\\s", "2"); // Adamastor, Maber (ou seria melhor "R"?)
            Translate("r", "R"); // Maria, Marcelo (ou seria melhor "2"?)

            Translate("(z)\\s", "S"); // Luiz, Tomaz
            Translate("z", "Z");

            Translate("(n)\\s", "M"); // Renan
            Translate("nh", "3");
            Translate("n", "N");

            Translate("ss", "S");
            Translate("\\s(s)", "S"); // sela, Sebastião
            Translate("(s)\\s", "S"); // mas, Marcos
            Translate("sh", "X"); // Koshi
            Translate(VOWEL + "(s)" + VOWEL, "Z"); // asa, Isabel
            Translate("sc[ei]", "S"); // asceta
            Translate("sc[aou]", "SC"); // masca
            Translate("s", "S");

            /* X é um pesadelo... por sorte não temos muitos nomes próprios com X */

            // Algumas sílabas e encontros como "ca", "ai" ou "ei" antes do X
            // parecem provocar o som de CH ao invés de KS
            Translate("[ckglrxaeiou][aeiou](x)", "X"); // abacaxi, Aleixo, Alexandre
            Translate("\\s(x)", "X"); // Xavier
            Translate("x\\s", "KS"); // Félix
            Translate("xc[ei]", "S"); // exceção, excelência, excitação
            Translate("\\se(x)" + VOWEL, "Z"); // exemplo, exercício, exímio
            Translate("\\se(x)" + NON_VOWEL, "S"); // êxtase, exposição
            // mexe, mexido... Uóxinton :D ... mas... e máximo e táxi? :(
            Translate("x[ei]", "X");
            Translate("x[aou]", "KS"); // sexo, anexo,
            Translate("x", "KS"); // o resto

            // O resto
            Translate("q", "K");
            Translate("\\sh(" + VOWEL + ")", THE_MATCH);
            Translate("w" + VOWEL, "V");
            Ignore("h");

            // Essas consoantes são fortes, tem o som que tem.
            Keep("b", "t", "p", "d", "f", "j", "k", "m", "v");

            // Vogal no começo é a própria vogal
            Translate("\\s(" + VOWEL + ")", THE_MATCH);

            // O resto das vogais são ignoradas
            Ignore(VOWEL);
        }
    }
}

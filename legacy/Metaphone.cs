//------------------------------------------------------------------------------
// <copyright file="CSSqlClassFile.cs" company="Microsoft">
//     Copyright (c) Microsoft Corporation.  All rights reserved.
// </copyright>
//------------------------------------------------------------------------------
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using System.Text.RegularExpressions;

namespace Metaphone_BR
{
    public abstract class Metaphone
    {

        protected internal const string THE_MATCH = "$0";
        protected internal const string VOWEL = "[aeiouy]";
        protected internal const string NON_VOWEL = "[^aeiouy]";
        private string original;
        private string transformed;
        private StringBuilder result;
        private int currentPosition;
        private bool hadMatches = false;
        private string currentMatch;

        public Metaphone(string text)
        {
            this.original = text;
            this.transformed = original;
            this.result = new StringBuilder();
            this.currentPosition = 0;
        }

        private void Calculate()
        {
            if (Blank)
            {
                return;
            }

            AllLowerCase();
            RemoveAccents();
            Prepare();
            AddSpaceToBorders();

            while (NotFullyProcessed)
            {
                Keep(" ");
                Algorithm();
                IgnoreNoMatches();
            }
        }

        protected internal abstract void Prepare();

        protected internal abstract void Algorithm();

        private bool FullyProcessed
        {
            get
            {
                return currentPosition >= transformed.Length;
            }
        }

        private bool NotFullyProcessed
        {
            get
            {
                return !FullyProcessed;
            }
        }

        private void IgnoreNoMatches()
        {
            if (!hadMatches)
            {
                currentPosition += 1;
            }
            hadMatches = false;
        }

        protected internal virtual void Translate(string pattern, string subst)
        {
            if (FullyProcessed || HadMatches())
            {
                return;
            }

            if (Regex.IsMatch(pattern, ".+\\(.*"))
            {
                LookBehind(pattern.Substring(0, pattern.IndexOf("(", StringComparison.Ordinal)));
                if (HadMatches())
                {
                    LookAhead(pattern.Substring(pattern.IndexOf("(", StringComparison.Ordinal)));
                }
            }
            else
            {
                LookAhead(pattern);
            }

            if (!HadMatches())
            {
                return;
            }

            subst = THE_MATCH.Equals(subst) ? CurrentMatch() : subst;
            Consume(CurrentMatch());
            result.Append(subst.ToUpper());
        }

        private void Consume(string match)
        {
            currentPosition += match.Length;
        }

        protected internal virtual void Ignore(string pattern)
        {
            Translate(pattern, "");
        }

        protected internal virtual void Keep(params string[] patterns)
        {
            Translate("(" + String.Join("|", patterns) + ")", THE_MATCH);
        }

        private bool HadMatches()
        {
            return hadMatches;
        }

        private string CurrentMatch()
        {
            return currentMatch;
        }

        private bool Matches(string pattern, string text)
        {
            Match match = Regex.Match(text, pattern);

            hadMatches = match.Success;

            if (hadMatches)
            {
                currentMatch = match.Value;
            }

            return hadMatches;
        }

        private void LookAhead(string pattern)
        {
            Matches("^" + pattern, AheadString());
        }

        private void LookBehind(string pattern)
        {
            Matches(pattern + "$", BehindString());
        }

        private string AheadString()
        {
            return transformed.Substring(currentPosition);
        }

        private string BehindString()
        {
            return transformed.Substring(0, currentPosition);
        }

        private bool Blank
        {
            get
            {
                return transformed == null || transformed.Length == 0;
            }
        }

        protected internal virtual void RemoveAccents()
        {
            Dictionary<string, string> substs = new Dictionary<string, string>();
            substs.Add("[âãáàäÂÃÁÀÄ]", "a");
            substs.Add("[éèêëÉÈÊË]", "e");
            substs.Add("[íìîïÍÌÎÏ]", "i");
            substs.Add("[óòôõöÓÒÔÕÖ]", "o");
            substs.Add("[úùûüÚÙÛÜ]", "u");

            string[] patterns = new string[substs.Keys.Count];
            substs.Keys.CopyTo(patterns, 0);
            string pattern = String.Join("|", patterns);

            var regex = new Regex(pattern);

            transformed = regex.Replace(transformed, m => substs[m.Value]);
        }

        protected internal virtual void RemoveMultiples(params string[] letters)
        {
            foreach (string letter in letters)
            {
                string pattern = letter + "{2,}";
                transformed = Regex.Replace(transformed, pattern, letter, RegexOptions.IgnoreCase);
            }
        }

        private void AddSpaceToBorders()
        {
            transformed = " " + transformed + " ";
        }

        private void AllLowerCase()
        {
            transformed = transformed.ToLower();
        }

        public override string ToString()
        {
            Calculate();
            return result.ToString().Trim();
        }
    }
}

using System;
using System.Collections.Generic;

namespace BusinessRuleDomain.RuleEngine
{
    public class BusinessRuleExecutor : IRuleExecutor
    {
        public List<RuleLog> Logs { get; set; } = new List<RuleLog>();

        public TResult Execute<TInput, TFact, TResult>(IRule<TInput, TFact, TResult> rule, TInput input, TFact fact)
        {
            var result = rule.Execute(input, fact);
            Logs.Add(new RuleLog
            {
                ExecutedTime = DateTime.Now,
                Expression =rule.Expression.ToString(),
                Facts = result.Facts,
                Input = result.Inputs,
                RuleName = result.RuleName,
                Result = result.Result.ToString()
            });


            return result.Result;

        }
    }
}

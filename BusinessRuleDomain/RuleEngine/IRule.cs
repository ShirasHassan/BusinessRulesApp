using System;
using System.Linq.Expressions;

namespace BusinessRuleDomain.RuleEngine
{
    public interface IRule<TInput, TFact, TResult>
    {
        string RuleType { get; set; }
        string Name { get; set; }
        string RuleDescription { get; set; }
        Expression<Func<TInput, TFact, TResult>> Expression { get; set; }
        BusinessRuleResult<TResult> Execute(TInput input, TFact fact);
    }
}
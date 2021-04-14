using System.Collections.Generic;

namespace BusinessRuleDomain.RuleEngine
{
    public interface IRuleExecutor
    {
         List<RuleLog>  Logs { get; }
        TResult Execute<TInput, TFact, TResult>(IRule<TInput, TFact, TResult> rule, TInput input, TFact fact);
    }
}
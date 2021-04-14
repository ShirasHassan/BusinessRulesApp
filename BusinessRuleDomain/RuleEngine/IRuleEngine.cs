using System;

namespace BusinessRuleDomain.RuleEngine
{
    public interface IRuleEngine 
    {
        Type InputType { get; }
        Type OutputType { get; }
        string FactName { get; }

        IRuleEngineResult Execute(IRuleEngineInput input, IRuleEngineFacts facts, IRuleExecutor executor);
    }
}
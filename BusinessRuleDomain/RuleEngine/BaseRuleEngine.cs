using System;

namespace BusinessRuleDomain.RuleEngine
{
    public abstract class BaseRuleEngine<TInput,TFact,TResult> : IRuleEngine
    where  TInput : IRuleEngineInput
    where TFact : IRuleEngineFacts
    where TResult : IRuleEngineResult
    {
        public Type InputType => typeof(TInput);
        public Type OutputType => typeof(TResult);
        public string FactName => typeof(TFact).Name;


        IRuleEngineResult IRuleEngine.Execute(IRuleEngineInput input, IRuleEngineFacts fact,
            IRuleExecutor executor) => Execute((TInput) input, (TFact) fact, executor);

        public abstract TResult Execute(TInput input, TFact fact, IRuleExecutor executor);

    }
}
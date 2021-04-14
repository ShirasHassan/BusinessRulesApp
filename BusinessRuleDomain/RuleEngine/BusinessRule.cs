using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using BusinessRuleDomain.RuleEngine.Models;

namespace BusinessRuleDomain.RuleEngine
{
    public class BusinessRule<TInput, TFact, TResult> : IRule<TInput, TFact, TResult> where TInput : IRuleEngineInput
    where TFact : IRuleEngineFacts
    {
        private readonly Lazy<Func<TInput, TFact, TResult>> _compiled;
        private readonly Lazy<Func<TInput, List<DataPoint>>> _inputGatherer;
        private readonly Lazy<Func<TFact, List<DataPoint>>> _factGatherer;

        public string RuleType { get; set; }
        public string Name { get; set; }
        public string RuleDescription { get; set; }
        public Expression<Func<TInput,TFact,TResult>> Expression { get; set; }

        public BusinessRule()
        {
            _compiled = new Lazy<Func<TInput, TFact, TResult>>(() => Expression.Compile());
            _inputGatherer = new Lazy<Func<TInput, List<DataPoint>>>(() => ExpressionBuilderHelper.GenerateInputDataPointsExpression(Expression).Compile());
            _factGatherer = new Lazy<Func<TFact, List<DataPoint>>>(() => ExpressionBuilderHelper.GenerateFactDataPointsExpression(Expression).Compile());
        }


        public BusinessRuleResult<TResult> Execute(IRuleEngineInput input, IRuleEngineFacts fact) => Execute((TInput)input, (TFact)fact);

        public  BusinessRuleResult<TResult> Execute(TInput input, TFact fact)
        {
            var result = _compiled.Value(input, fact);
            var inputDataPoints = _inputGatherer.Value(input);
            var factDataPoints = _factGatherer.Value(fact);

            return new BusinessRuleResult<TResult> { Inputs = inputDataPoints, Result = result , Facts = factDataPoints , RuleName = Name };

        }
    }
}

using System;
using System.Collections.Generic;
using BusinessRuleDomain.RuleEngine;
using BusinessRuleDomain.RuleRequestHandler.DiscountPolicies;

namespace BusinessRuleDomain.RuleRequestHandler
{
    public class RuleEngineFactory : IRuleEngineFactory
    {
        private Dictionary<string, IRuleEngine> _engineCollection;
        private Dictionary<string, BaseRuleEngineFacts> _engineFactsCollection;

        public RuleEngineFactory()
        {
            _engineCollection = new Dictionary<string, IRuleEngine>() {
                { nameof(DiscountEngine), new DiscountEngine()}
            };

            _engineFactsCollection = new Dictionary<string, BaseRuleEngineFacts>() {
                { nameof(DiscountPolicyFacts), new DiscountPolicyFacts() }
            };
        }

        public IRuleEngine GetRuleEngine(string ruleEngineName)
        {
            return _engineCollection[ruleEngineName];
        }

        public IRuleEngineFacts GetRuleEngineFact(string ruleEngineFact)
        {
            var fact = _engineFactsCollection[ruleEngineFact];
            fact.LoadDefaults();
            return fact;
        }
    }
}

using System;
namespace BusinessRuleDomain.RuleEngine
{
    public interface IRuleEngineFactory
    {
        IRuleEngine GetRuleEngine(string ruleEngineName);

        IRuleEngineFacts GetRuleEngineFact(string ruleEngineFact);
    }
}

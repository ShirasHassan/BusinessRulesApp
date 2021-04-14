using System;
using System.Threading.Tasks;
using BusinessRuleDomain.RuleEngine;
using Newtonsoft.Json;

namespace BusinessRuleDomain.RuleRequestHandler
{
    public class BusinessRuleRequestHandler : IRequestHandler
    {
        private IRuleExecutor ruleExecutor { get; set; }
        private IRuleEngineFactory ruleEngineFactory { get; set; }

        public BusinessRuleRequestHandler()
        {
            this.ruleExecutor = new BusinessRuleExecutor();
            this.ruleEngineFactory = new RuleEngineFactory();
        }

        public async Task<IRuleEngineResult> Handle(RuleRequest request)
        {
            var ruleEngine = ruleEngineFactory.GetRuleEngine(request.RuleName);
            var input = (IRuleEngineInput) request.Input.ToObject(ruleEngine.InputType);
            var facts = ruleEngineFactory.GetRuleEngineFact(ruleEngine.FactName);
            var results = ruleEngine.Execute(input, facts, ruleExecutor);
            string json = JsonConvert.SerializeObject(ruleExecutor.Logs, Formatting.Indented);
            Console.Write(json);
            return results;
            
        }
    }
}

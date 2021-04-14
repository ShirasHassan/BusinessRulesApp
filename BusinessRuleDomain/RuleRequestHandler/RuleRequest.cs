using System;
using Newtonsoft.Json.Linq;

namespace BusinessRuleDomain.RuleRequestHandler
{
    public class RuleRequest
    {
        public Guid RequestId { get; set; }
        public Guid WorkflowIdentifier { get; set; }
        public string RuleName { get; set; }
        public JObject Input { get; set; }

    }
}

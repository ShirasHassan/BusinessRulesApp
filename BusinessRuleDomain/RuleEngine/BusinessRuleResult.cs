using System;
using System.Collections.Generic;
using BusinessRuleDomain.RuleEngine.Models;

namespace BusinessRuleDomain.RuleEngine
{
    public class BusinessRuleResult<TResult>
    {
        public string RuleName { get; set; }
        public List<DataPoint> Inputs { get; set; }
        public List<DataPoint> Facts { get; set; }
        public TResult Result { get; set; }
    }
}

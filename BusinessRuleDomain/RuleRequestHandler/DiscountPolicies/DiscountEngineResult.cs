using System;
using BusinessRuleDomain.RuleEngine;

namespace BusinessRuleDomain.RuleRequestHandler.DiscountPolicies
{
    public class DiscountEngineResult : IRuleEngineResult
    {
        public bool IsFirstTimeDiscountApplied { get; set; }
        public bool IsBulkPuchaseDiscountApplied { get; set; }
        public bool IsFrequentPurchaseDiscountApplied { get; set; }
        public decimal DiscountApplied { get; set; }
    }
}

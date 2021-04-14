using System;
using BusinessRuleDomain.RuleEngine;

namespace BusinessRuleDomain.RuleRequestHandler.DiscountPolicies
{
    public class CustomerInfo : IRuleEngineInput
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public int PurchaseCount { get; set; }
        public decimal BilledAmount { get; set; }
        public decimal MaxAdjustmentsAllowed { get; set; }
    }
}

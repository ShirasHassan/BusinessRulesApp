using System;
using BusinessRuleDomain.RuleEngine;

namespace BusinessRuleDomain.RuleRequestHandler.DiscountPolicies
{
    public class DiscountPolicyFacts : BaseRuleEngineFacts
    {
        public decimal NewCustomerDiscount { get; set; }
        public decimal FrequentCustomerDiscount { get; set; }
        public int FrequentCustomerMinPurchaseCount { get; set; }
        public decimal BulkPurchaseDiscount { get; set; }
        public decimal BulkPurchaseThreshold { get; set; }

        public override void LoadDefaults()
        {
            NewCustomerDiscount = 0.10m;
            FrequentCustomerDiscount = 0.07m;
            FrequentCustomerMinPurchaseCount = 10;
            BulkPurchaseDiscount = .10m;
            BulkPurchaseThreshold = 10000m;
        }
    }
}

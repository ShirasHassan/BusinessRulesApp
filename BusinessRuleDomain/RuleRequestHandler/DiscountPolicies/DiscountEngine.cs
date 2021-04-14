using System;
using BusinessRuleDomain.RuleEngine;

namespace BusinessRuleDomain.RuleRequestHandler.DiscountPolicies
{
    public class DiscountEngine : BaseRuleEngine<CustomerInfo, DiscountPolicyFacts, DiscountEngineResult>
    {
        private IRule<CustomerInfo, DiscountPolicyFacts, decimal> _firstTimeCustomerPolicy;
        private IRule<CustomerInfo, DiscountPolicyFacts, decimal> _frequentCustomerPolicy;
        private IRule<CustomerInfo, DiscountPolicyFacts, decimal> _bulkPurchasePolicy;

        public DiscountEngine()
        {
            _firstTimeCustomerPolicy = new BusinessRule<CustomerInfo, DiscountPolicyFacts, decimal>() {
                 Name = "FirstTimeCustomerPolicy",
                RuleDescription ="discounts for new customer",
                RuleType ="discount_policy",
                Expression = (input,fact) => input.PurchaseCount == default ? fact.NewCustomerDiscount : default
            };
            _frequentCustomerPolicy = new BusinessRule<CustomerInfo, DiscountPolicyFacts, decimal>()
            {
                Name = "FrequentCustomerPolicy",
                RuleDescription = "discounts for loyal customer",
                RuleType = "discount_policy",
                Expression = (input, fact) => input.PurchaseCount >= fact.FrequentCustomerMinPurchaseCount ? fact.FrequentCustomerDiscount : default
            };
            _bulkPurchasePolicy = new BusinessRule<CustomerInfo, DiscountPolicyFacts, decimal>()
            {
                Name = "BulkPurchasePolicy",
                RuleDescription = "discounts for bulk puchasing customer",
                RuleType = "discount_policy",
                Expression = (input, fact) => input.BilledAmount >= fact.BulkPurchaseThreshold ? fact.BulkPurchaseDiscount : default
            };
        }

        public override DiscountEngineResult Execute(CustomerInfo input, DiscountPolicyFacts fact, IRuleExecutor executor)
        {
           var firstTimeCustomerDiscount = executor.Execute(_firstTimeCustomerPolicy,input, fact);
            var frequentCustomerDiscount = executor.Execute(_frequentCustomerPolicy, input, fact);
            var bulkPurchaseDiscount = executor.Execute(_bulkPurchasePolicy, input, fact);
            return new DiscountEngineResult {
                IsBulkPuchaseDiscountApplied = bulkPurchaseDiscount != default,
                IsFirstTimeDiscountApplied = firstTimeCustomerDiscount != default,
                IsFrequentPurchaseDiscountApplied = frequentCustomerDiscount != default,
                DiscountApplied = input.MaxAdjustmentsAllowed * (firstTimeCustomerDiscount + frequentCustomerDiscount + bulkPurchaseDiscount)
            };
        }
    }
}

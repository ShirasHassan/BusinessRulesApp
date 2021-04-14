using System;
namespace BusinessRuleDomain.RuleEngine
{
    public abstract class BaseRuleEngineFacts : IAggregateDocument, IRuleEngineFacts
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public Guid VersionId { get; set; } = Guid.NewGuid();
        public String FactName => this.GetType().Name;
        public DateTime CreatedOn { get; set; } = DateTime.Now.Date;
        public DateTime EffectiveOn { get; set; } = DateTime.Now.Date;
        public DateTime ExpiredOn { get; set; } = DateTime.MaxValue.Date;
        public abstract void LoadDefaults();
    }
}

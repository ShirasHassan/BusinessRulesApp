using System;
using MongoDB.Bson.Serialization.Attributes;

namespace BusinessRuleDomain.RuleEngine
{
    public interface IRuleEngineFacts
    {
        [BsonDateTimeOptions(DateOnly =true)]
        DateTime EffectiveOn { get; }

        [BsonDateTimeOptions(DateOnly = true)]
        DateTime ExpiredOn { get; }

        static IRuleEngineFacts Defaults { get; }
    }
}
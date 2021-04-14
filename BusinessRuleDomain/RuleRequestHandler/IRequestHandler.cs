using System;
using System.Threading.Tasks;
using BusinessRuleDomain.RuleEngine;

namespace BusinessRuleDomain.RuleRequestHandler
{
    public interface IRequestHandler
    {
        Task<IRuleEngineResult> Handle(RuleRequest request);
    }
}

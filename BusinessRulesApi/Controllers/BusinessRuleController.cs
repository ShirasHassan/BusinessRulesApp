using System;
using BusinessRuleDomain.RuleEngine;
using BusinessRuleDomain.RuleRequestHandler;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using Swashbuckle.AspNetCore.Annotations;

namespace BusinessRulesApi.Controllers
{
    [ApiVersionNeutral]
    [ApiController]
    [Produces("application/json")]
    [Route("v{version:apiversion}/[controller]")]
    public class BusinessRuleController : ControllerBase
    {
        /// <summary>
        /// Execute Rule
        /// </summary>
        /// <param name="request"></param>
        /// <returns></returns>
        [SwaggerResponse(StatusCodes.Status200OK, "Returns destination object",typeof(IRuleEngineResult))]
        [SwaggerResponse(StatusCodes.Status404NotFound, "Returns messagebag object with error object")]
        [HttpPost]
        public IRuleEngineResult Post(RuleRequest request)
        {
            var rng = new Random();
            var handler = new BusinessRuleRequestHandler();

            return handler.Handle(request).Result;
        }

        // Sample
        /*{
            "requestId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "workflowIdentifier": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "ruleName": "DiscountEngine",
            "input": {
                "age": 35,
                "billedAmount": 100000000,
                "maxAdjustmentsAllowed": 0.20,
                "name": "Shiras",
                "purchaseCount": 100
            }
        }*/
    }
}
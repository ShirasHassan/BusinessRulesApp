using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BusinessRuleDomain.RuleRequestHandler;
using BusinessRuleDomain.RuleRequestHandler.DiscountPolicies;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json.Linq;
using Swashbuckle.AspNetCore.Annotations;

namespace BusinessRulesApi.Controllers
{
    [ApiVersion("1.0")]
    [ApiVersion("2.0")]
    [ApiController]
    [Produces("application/json")]
    [Route("v{version:apiversion}/[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        /// <summary>
        /// test 
        /// </summary>
        /// <returns></returns>
        [SwaggerResponse(StatusCodes.Status200OK, "Returns destination object")]
        [SwaggerResponse(StatusCodes.Status404NotFound, "Returns messagebag object with error object")]
        [MapToApiVersion("1")]
        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = Summaries[rng.Next(Summaries.Length)]
            })
            .ToArray();
        }

        [SwaggerResponse(StatusCodes.Status200OK, "Returns destination object")]
        [SwaggerResponse(StatusCodes.Status404NotFound, "Returns messagebag object with error object")]
        [MapToApiVersion("2")]
        [HttpGet]
        public IEnumerable<WeatherForecast> Get2()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = Summaries[rng.Next(Summaries.Length)]
            })
            .ToArray();
        }
    }
}

using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace BusinessRulesApi.Middleware.CustomSwagger {
    public class SwaggerOperationFilter : IOperationFilter {
        public void Apply (OpenApiOperation operation, OperationFilterContext context) {
            if (operation.Parameters == null) {
                operation.Parameters = new List<OpenApiParameter> ();
            }

            operation.Parameters.Add (new OpenApiParameter {
                Name = "Authorization",
                    In = ParameterLocation.Header,
                    Schema = new OpenApiSchema { Type = "strng" },
                    Required = false
            });
        }
    }
}
using System;
using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc.ApiExplorer;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;
using Swashbuckle.AspNetCore.SwaggerUI;

namespace BusinessRulesApi.Middleware.CustomSwagger
{
    public static class SwaggerExtensions {
        private const string SettingsSectionName = "SwaggerSettings";

        #region EnableSwaggerMiddleware
        public static IApplicationBuilder UseCustomSwagger (this IApplicationBuilder app, string serviceName) {
            app.UseSwagger (options => { options.RouteTemplate = $"{serviceName}/swagger/{{documentName}}/swagger.json"; });
            app.UseSwaggerUI (options => EnableSwaggerEndPoint (options, app, serviceName));
            app.UseReDoc(option => {
                option.RoutePrefix = $"{serviceName}/api-docs";
                option.SpecUrl($"../swagger/v1/swagger.json");
            });
            return app;
        }

        public static IApplicationBuilder UseCustomSwagger (this IApplicationBuilder app, IConfiguration configuration) {
            app.UseSwagger ();
            app.UseSwaggerUI (options => EnableSwaggerEndPoint (options, app, configuration : configuration));
            return app;
        }

        private static void EnableSwaggerEndPoint (SwaggerUIOptions options, IApplicationBuilder applicationBuilder, string serviceName = "", IConfiguration configuration = null) {

            var provider = applicationBuilder.ApplicationServices.GetRequiredService<IApiVersionDescriptionProvider> ();
            var routePrefix = serviceName != string.Empty ? $"{serviceName}/swagger" : string.Empty;
            var settings = configuration != null ? configuration.GetSection (SettingsSectionName).Get<SwaggerSettings> () : new SwaggerSettings ();
            serviceName ??= settings.ServiceName;

            foreach (var description in provider.ApiVersionDescriptions) {
                options.SwaggerEndpoint ($"{description.GroupName}/swagger.json", $"{serviceName} API {description.GroupName}");
                if (!string.IsNullOrEmpty (routePrefix)) {
                    options.RoutePrefix = $"{routePrefix}";
                }
            }
        }
        #endregion EnableSwaggerMiddleware

        #region ConfigureSwagger
        public static IServiceCollection AddCustomSwagger (this IServiceCollection services, IConfiguration configuration, Type startupType) {
            return services
                .AddSwaggerGen (options => ConfigureSwagger (options, services, configuration, startupType))
                .AddSwaggerGenNewtonsoftSupport();
        }

        private static void ConfigureSwagger (SwaggerGenOptions options, IServiceCollection services, IConfiguration configuration, Type startupType) {
            var settings = configuration.GetSection (SettingsSectionName).Get<SwaggerSettings> ();
            var provider = services.BuildServiceProvider ().GetRequiredService<IApiVersionDescriptionProvider> ();
            foreach (var description in provider.ApiVersionDescriptions) {
                options.SwaggerDoc (description.GroupName, GetOpenApiInfo (description, settings));
            }
            options.OperationFilter<SwaggerOperationFilter> ();
            options.SchemaFilter<SwaggerSchemaFilter> ();
            options.EnableAnnotations ();
            options.IncludeXmlComments (GetXmlDocumentationFile (startupType));
        }

        private static string GetXmlDocumentationFile (Type startupType) {
            var basePath = AppContext.BaseDirectory;
            var xmlName = $"{startupType.Assembly.GetName().Name}.xml";
            return Path.Combine (basePath, xmlName);
        }

        private static OpenApiInfo GetOpenApiInfo (ApiVersionDescription description, SwaggerSettings settings) {
            return new OpenApiInfo () {
                Title = $"{settings.ServiceName} API {description.ApiVersion}",
                    Version = description.ApiVersion.ToString (),
                    Description = description.IsDeprecated == true ? "This Api version has been deprecated." : $"Handles {settings.ServiceName} responsibilities.",
                    Contact = new OpenApiContact () {
                    Name = settings.ContactName,
                    Email = settings.ContactEmail,
                    Url = new Uri (settings.ContactUrl)
                    }
            };
        }
        #endregion ConfigureSwagger
    }
}
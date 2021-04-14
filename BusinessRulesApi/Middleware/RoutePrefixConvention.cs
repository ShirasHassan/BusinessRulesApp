using System;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ApplicationModels;

namespace BusinessRulesApi.Middleware
{
    public class RoutePrefixConvention : IApplicationModelConvention
    {
        private readonly AttributeRouteModel _attributeRouteModel;
        public RoutePrefixConvention(RouteAttribute routeAttribute)
        {
            this._attributeRouteModel = new AttributeRouteModel(routeAttribute);
        }
        public void Apply(ApplicationModel application)
        {
            foreach (var selector in application.Controllers.SelectMany(c => c.Selectors))
            {
                if (selector.AttributeRouteModel == null)
                {
                    selector.AttributeRouteModel = _attributeRouteModel;
                }
                else
                {
                    selector.AttributeRouteModel = AttributeRouteModel.CombineAttributeRouteModel(_attributeRouteModel,
                        selector.AttributeRouteModel);
                }
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Reflection;

namespace BusinessRuleDomain.RuleEngine
{
    public class ParameterVisitor : ExpressionVisitor
    {
        private readonly string _parameterName;
        public ParameterVisitor(string parameterName)
        {
            _parameterName = parameterName;
        }

        public HashSet<PropertyInfo> Members { get; } = new HashSet<PropertyInfo>();

        protected override Expression VisitMember(MemberExpression node)
        {
            if(node.Expression.NodeType == ExpressionType.Parameter)
            {
                var parameterExpression = node.Expression as ParameterExpression;
               if( parameterExpression.Name == _parameterName)
                {
                    Members.Add((PropertyInfo)node.Member);
                }

            }
            return base.VisitMember(node);
        }
    }
}

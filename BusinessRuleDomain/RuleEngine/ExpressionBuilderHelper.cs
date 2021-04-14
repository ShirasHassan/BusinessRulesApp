using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;
using BusinessRuleDomain.RuleEngine.Models;

namespace BusinessRuleDomain.RuleEngine
{


    public static class ExpressionBuilderHelper
    {
        private static readonly ConstructorInfo _listOfDataPointConstructor = typeof(List<DataPoint>).GetConstructor(new Type[0]);
        private static readonly ConstructorInfo _dataPointConstructor = typeof(DataPoint).GetConstructor(new Type[0]);
        private static readonly PropertyInfo _nameProperty = typeof(DataPoint).GetProperty(nameof(DataPoint.Name));
        private static readonly PropertyInfo _valueProperty = typeof(DataPoint).GetProperty(nameof(DataPoint.Value));

        internal static Expression<Func<TInput, List<DataPoint>>> GenerateInputDataPointsExpression<TInput, TFact, TResult>(Expression<Func<TInput, TFact, TResult>> expression)
        {
            var inputParam = expression.Parameters[0];
            var inputParamExpressions = new ParameterVisitor(inputParam.Name);
            inputParamExpressions.Visit(expression);

            return input => new List<DataPoint> (inputParamExpressions.Members.Select( m => new DataPoint() {
                                                                                        Name = m.Name,
                                                                                        Value = m.GetValue(input, null)
                                                                                        }));


            //return Expression.Lambda<Func<TInput, List<DataPoint>>>(body:
            //            Expression.ListInit(newExpression: Expression.New(_listOfDataPointConstructor), initializers: inputParamExpressions.Members.Select(m =>
            //                Expression.MemberInit(newExpression: Expression.New(_dataPointConstructor),
            //                        Expression.Bind(_nameProperty, Expression.Constant(m.Name)),
            //                        Expression.Bind(_valueProperty, Expression.Convert(expression: Expression.Property(inputParam, m), typeof(object))))
            //            )), inputParam);


        }

        internal static Expression<Func<TFact, List<DataPoint>>> GenerateFactDataPointsExpression<TInput, TFact, TResult>(Expression<Func<TInput, TFact, TResult>> expression)
        {
            var factParam = expression.Parameters[1];
            var factParamExpression = new ParameterVisitor(factParam.Name);
            factParamExpression.Visit(expression);

            return Expression.Lambda<Func<TFact, List<DataPoint>>>(body:
                Expression.ListInit(newExpression: Expression.New(_listOfDataPointConstructor), initializers: factParamExpression.Members.Select(m =>
                 Expression.MemberInit(newExpression: Expression.New(_dataPointConstructor),
                           Expression.Bind(_nameProperty, Expression.Constant(m.Name)),
                           Expression.Bind(_valueProperty, Expression.Convert(expression: Expression.Property(factParam, m), typeof(object))))
                )), factParam);
        }
    }
}

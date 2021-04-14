using System;
using System.Collections.Generic;
using BusinessRuleDomain.RuleEngine.Models;

namespace BusinessRuleDomain.RuleEngine
{
    public class RuleLog
    {

        public string RuleName  { get; set; }
        public List<DataPoint> Facts { get; set; }
        public List<DataPoint> Input { get; set; }
        public string Expression { get; set; }
        public DateTime ExecutedTime { get; set; }
        public string Result { get; set; }
    }
}

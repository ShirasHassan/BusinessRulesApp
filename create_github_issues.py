#!/usr/bin/env python3
"""
Script to create GitHub Issues for BusinessRulesApp with detailed specs.

Usage:
    GITHUB_TOKEN=<your_pat> python3 create_github_issues.py

Requirements:
    pip install requests
"""

import os
import sys
import json
import time
import requests

REPO = "ShirasHassan/BusinessRulesApp"
API_BASE = "https://api.github.com"

ISSUES = [
    # ─────────────────────────────────────────────────────────────────────────
    # FRAMEWORK & DEPENDENCY UPGRADES
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "[Upgrade] Migrate from .NET Core 3.1 / .NET Standard 2.1 to .NET 10",
        "labels": ["upgrade", "breaking-change"],
        "body": """\
## Summary
The project currently targets **`netcoreapp3.1`** (API) and **`netstandard2.1`** (Domain), both of which are end-of-life.
Migrate both projects to **.NET 10** (latest LTS, supported until November 2028).

## Current State
| Project | Target Framework | Status |
|---|---|---|
| `BusinessRulesApi` | `netcoreapp3.1` | ❌ End-of-Life |
| `BusinessRuleDomain` | `netstandard2.1` | ❌ End-of-Life |

## Target State
| Project | Target Framework |
|---|---|
| `BusinessRulesApi` | `net10.0` |
| `BusinessRuleDomain` | `net8.0` (or `net10.0`) |

## Implementation Steps
1. Update `BusinessRulesApi/BusinessRulesApi.csproj`:
   - Change `<TargetFramework>netcoreapp3.1</TargetFramework>` → `<TargetFramework>net10.0</TargetFramework>`
   - Update `<DocumentationFile>` path accordingly
2. Update `BusinessRuleDomain/BusinessRuleDomain.csproj`:
   - Change `<TargetFramework>netstandard2.1</TargetFramework>` → `<TargetFramework>net10.0</TargetFramework>`
3. Update `Startup.cs` / `Program.cs` to use the .NET 10 minimal hosting model (remove `Startup.cs`, move everything to `Program.cs` using `WebApplication.CreateBuilder`).
4. Fix any compilation errors from breaking changes.
5. Run and verify the application starts correctly.

## Acceptance Criteria
- [ ] Both projects target `net10.0`
- [ ] Application builds with zero warnings/errors
- [ ] Swagger UI loads and works
- [ ] `/v1/businessrule` endpoint responds correctly
""",
    },
    {
        "title": "[Upgrade] Upgrade Swashbuckle.AspNetCore from 5.4.1 to 10.x",
        "labels": ["upgrade", "breaking-change"],
        "body": """\
## Summary
`Swashbuckle.AspNetCore` is currently on **v5.4.1**. Latest stable is **v10.1.5**.
This is a major version jump with breaking changes around the OpenAPI 3.1 migration.

## Current Versions
```xml
<PackageReference Include="Swashbuckle.AspNetCore" Version="5.4.1" />
<PackageReference Include="Swashbuckle.AspNetCore.Annotations" Version="5.4.1" />
<PackageReference Include="Swashbuckle.AspNetCore.Newtonsoft" Version="5.4.1" />
<PackageReference Include="Swashbuckle.AspNetCore.ReDoc" Version="5.4.1" />
```

## Target Versions
All packages → `10.1.5`

## Breaking Changes to Address
- `Microsoft.OpenApi` upgraded to **2.x** (OpenAPI 3.1 support); non-nullable `OpenApiDocument` properties changed.
- `OpenApiSchema` property nullability changes.
- `WithOpenApi()` method removed; reference handling changed.
- **Staged upgrade recommended**: upgrade to `9.0.6` first, then `10.1.5`.

## Implementation Steps
1. Stage 1 — Upgrade to `9.0.6`:
   - Update all four Swashbuckle packages to `9.0.6`.
   - Fix compilation errors.
   - Verify Swagger UI still loads.
2. Stage 2 — Upgrade to `10.1.5`:
   - Update all packages to `10.1.5`.
   - Update `SwaggerOperationFilter.cs`: replace `OpenApiSchema { Type = "strng" }` with `OpenApiSchema { Type = "string" }` *(also fixes the existing typo bug)*.
   - Update `SwaggerSchemaFilter.cs` and `SwaggerExtensions.cs` for new API surface.
   - If OpenAPI 3.1 output is needed: add `UseSwagger(options => { options.OpenApiVersion = OpenApiSpecVersion.OpenApi3_1; })`.
3. Run smoke tests to confirm Swagger UI and ReDoc render correctly.

## Acceptance Criteria
- [ ] All Swashbuckle packages at `10.1.5`
- [ ] Swagger UI and ReDoc load without errors
- [ ] `SwaggerOperationFilter.cs` uses `"string"` (not `"strng"`)
- [ ] OpenAPI spec validates correctly
""",
    },
    {
        "title": "[Upgrade] Replace deprecated Microsoft.AspNetCore.Mvc.Versioning with Asp.Versioning.Mvc 8.x",
        "labels": ["upgrade", "breaking-change"],
        "body": """\
## Summary
`Microsoft.AspNetCore.Mvc.Versioning` (`4.1.1`) is **deprecated**. The package maintainer left Microsoft and the project moved to a new package name.
Migrate to **`Asp.Versioning.Mvc` 8.1.1** and **`Asp.Versioning.Mvc.ApiExplorer` 8.1.1**.

## Current Packages (deprecated)
```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.Versioning" Version="4.1.1" />
<PackageReference Include="Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer" Version="4.1.1" />
```

## Target Packages
```xml
<PackageReference Include="Asp.Versioning.Mvc" Version="8.1.1" />
<PackageReference Include="Asp.Versioning.Mvc.ApiExplorer" Version="8.1.1" />
```

## Breaking Changes / Migration Notes
- Namespace changes: `Microsoft.AspNetCore.Mvc.Versioning.*` → `Asp.Versioning.*`
- Registration change: `AddApiVersioning()` call needs updating — `AddMvc()` at the end of `AddApiVersioning` is critical in new API.
- Migration guide: https://github.com/dotnet/aspnet-api-versioning/wiki/Migration

## Implementation Steps
1. Remove old packages from `BusinessRulesApi.csproj`, add new ones.
2. Update `using` statements across all files:
   - `Startup.cs` versioning setup
   - `SwaggerExtensions.cs` where `IApiVersionDescriptionProvider` is used
3. Update `services.AddApiVersioning(...)` call syntax per migration guide.
4. Verify versioned endpoints still route correctly (e.g., `/v1/businessrule`).

## Acceptance Criteria
- [ ] Old packages removed; new packages added at `8.1.1`
- [ ] Zero compilation errors
- [ ] API versioning works: `/v1/businessrule` returns correct response
- [ ] Swagger displays correct version information
""",
    },
    {
        "title": "[Upgrade] Upgrade Microsoft.AspNetCore.Mvc.NewtonsoftJson from 3.1.14 to 10.0.x",
        "labels": ["upgrade"],
        "body": """\
## Summary
`Microsoft.AspNetCore.Mvc.NewtonsoftJson` is on **3.1.14** (tied to .NET Core 3.1). After the .NET 10 migration, upgrade to **10.0.5**.

## Current Version
```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.NewtonsoftJson" Version="3.1.14" />
```

## Target Version
```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.NewtonsoftJson" Version="10.0.5" />
```

## Implementation Steps
1. This upgrade is **dependent on** the `.NET 10 framework upgrade` issue.
2. Update version in `BusinessRulesApi.csproj` after framework upgrade.
3. Verify JSON serialization still works correctly for `RuleRequest` / `IRuleEngineResult`.
4. Confirm `JObject` deserialization in `RuleRequest.Input` is unaffected.

## Acceptance Criteria
- [ ] Package at `10.0.5`
- [ ] JSON serialization/deserialization works correctly
- [ ] No breaking changes in Newtonsoft.Json behavior
""",
    },
    {
        "title": "[Upgrade] Upgrade MongoDB.Driver from 2.12.2 to 3.x or remove unused dependency",
        "labels": ["upgrade", "cleanup"],
        "body": """\
## Summary
`MongoDB.Driver` is referenced at **2.12.2** but **no MongoDB code exists** in the codebase. Latest version is **3.7.0** with breaking changes.

Two options exist:
- **Option A (Recommended)**: Remove the unused dependency entirely.
- **Option B**: Upgrade to `3.7.0` if MongoDB integration is planned.

## Current State
```xml
<!-- BusinessRuleDomain.csproj -->
<PackageReference Include="MongoDB.Driver" Version="2.12.2" />
```
- `IAggregateDocument.cs` interface exists (references MongoDB concept) but is never implemented or used.
- No `MongoClient`, `IMongoDatabase`, or collection code exists anywhere.

## Option A — Remove (Recommended)
1. Remove `<PackageReference Include="MongoDB.Driver" Version="2.12.2" />` from `BusinessRuleDomain.csproj`.
2. Delete or repurpose `IAggregateDocument.cs` (remove the MongoDB `ObjectId` import if present).
3. Verify build succeeds.

## Option B — Upgrade to 3.7.0 (if MongoDB needed)
1. Update version to `3.7.0`.
2. Address breaking changes:
   - MongoDB Server 4.2+ required.
   - TLS 1.0/1.1 no longer supported (must use TLS 1.2+).
   - Various driver API changes. See: https://www.mongodb.com/docs/drivers/csharp/current/reference/upgrade/v3/
3. Implement actual MongoDB integration with connection string in `appsettings.json`.

## Acceptance Criteria (Option A)
- [ ] MongoDB.Driver removed from `BusinessRuleDomain.csproj`
- [ ] `IAggregateDocument.cs` updated or removed
- [ ] Build succeeds with zero errors
""",
    },
    {
        "title": "[Upgrade] Upgrade Newtonsoft.Json from 13.0.1 to 13.0.4",
        "labels": ["upgrade"],
        "body": """\
## Summary
`Newtonsoft.Json` is on **13.0.1**. Latest stable is **13.0.4** with bug fixes and new features.

## Current Version
```xml
<PackageReference Include="Newtonsoft.Json" Version="13.0.1" />
```

## Target Version
```xml
<PackageReference Include="Newtonsoft.Json" Version="13.0.4" />
```

## What's New in 13.0.4
- `DateOnly` / `TimeOnly` support
- `JsonSelectSettings` for regex timeout configuration
- Improved memory allocation
- Index support with `JArray`
- AOT/trim compatibility annotations

## Known Concern
A reported issue in `13.0.4`: `NullValueHandling` in `SerializerSettings` may not be respected in `ToObject<T>()`. Test carefully after upgrade.

## Implementation Steps
1. Update version in `BusinessRuleDomain.csproj`.
2. Run existing tests (once added) to verify serialization behavior is unchanged.
3. Specifically validate `JsonConvert.SerializeObject(ruleExecutor.Logs, Formatting.Indented)` in `BusinessRuleRequestHandler.cs`.

## Acceptance Criteria
- [ ] Package at `13.0.4`
- [ ] JSON serialization of rule logs unchanged
- [ ] No regression in `RuleRequest.Input` (JObject) deserialization
""",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # BUG FIXES
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "[Bug] Fix typo 'strng' → 'string' in SwaggerOperationFilter",
        "labels": ["bug"],
        "body": """\
## Summary
A typo in `SwaggerOperationFilter.cs` sets the OpenAPI schema type to `"strng"` instead of `"string"`, producing an invalid OpenAPI spec.

## Location
`BusinessRulesApi/Middleware/CustomSwagger/SwaggerOperationFilter.cs`, line 15

## Current Code
```csharp
Schema = new OpenApiSchema { Type = "strng" }
```

## Fix
```csharp
Schema = new OpenApiSchema { Type = "string" }
```

## Impact
- The OpenAPI specification is technically invalid.
- API clients generated from the spec may behave incorrectly for affected parameters.
- Swagger UI validation warnings may appear.

## Implementation Steps
1. Open `SwaggerOperationFilter.cs`.
2. Replace `"strng"` with `"string"` on the affected line.
3. Verify Swagger UI displays the correct type for the parameter.

## Acceptance Criteria
- [ ] `"strng"` replaced with `"string"`
- [ ] OpenAPI spec validates without type errors
""",
    },
    {
        "title": "[Bug] Fix deadlock-prone .Result blocking call in BusinessRuleController",
        "labels": ["bug", "async"],
        "body": """\
## Summary
`BusinessRuleController.Execute()` calls `.Result` on an async `Task`, which can cause **deadlocks** under ASP.NET Core's synchronization context, especially under load.

## Location
`BusinessRulesApi/Controllers/BusinessRuleController.cs`, line 28-30

## Current Code (Problematic)
```csharp
[HttpPost]
public IActionResult Execute([FromBody] RuleRequest request)
{
    var rng = new Random();            // ← unused variable
    var handler = new BusinessRuleRequestHandler();
    return Ok(handler.Handle(request).Result);  // ← .Result blocks async → deadlock risk
}
```

## Fix
```csharp
[HttpPost]
public async Task<IActionResult> Execute([FromBody] RuleRequest request)
{
    var handler = new BusinessRuleRequestHandler();
    var result = await handler.Handle(request);
    return Ok(result);
}
```

## Additional Changes
- Remove the unused `var rng = new Random();` line.
- Add `using System.Threading.Tasks;` if not already present.

## Impact
Without this fix, under high concurrency the thread pool can be exhausted, leading to request hangs and service outages.

## Acceptance Criteria
- [ ] Controller action is `async Task<IActionResult>`
- [ ] `await` used instead of `.Result`
- [ ] Unused `rng` variable removed
- [ ] No deadlock under concurrent load
""",
    },
    {
        "title": "[Bug] Validate discount stacking logic to respect MaxAdjustmentsAllowed",
        "labels": ["bug", "business-logic"],
        "body": """\
## Summary
`DiscountEngine` applies three discount policies independently and sums their results multiplied by `MaxAdjustmentsAllowed`. When multiple policies apply simultaneously, the combined discount can **exceed 100%** or violate the intended cap.

## Location
`BusinessRuleDomain/RuleRequestHandler/DiscountPolicies/DiscountEngine.cs`

## Current Logic
```csharp
var total = MaxAdjustmentsAllowed * (discount1 + discount2 + discount3);
```
If all three discounts apply (10% + 7% + 10% = 27%), and `MaxAdjustmentsAllowed` > 1, the result is uncapped.

## Fix
```csharp
var rawTotal = discount1 + discount2 + discount3;
var total = Math.Min(rawTotal, MaxAdjustmentsAllowed);
```
Or define a separate `MaxCombinedDiscount` threshold.

## Implementation Steps
1. Clarify the intended business rule: should discounts stack or use the highest applicable discount?
2. Implement one of:
   - **Clamp**: `total = Math.Min(combinedDiscount, MaxAdjustmentsAllowed)`
   - **Max wins**: take the highest single discount that applies
   - **Priority order**: apply the first matching policy only
3. Add unit tests to cover:
   - No discount applies
   - Single discount applies
   - Multiple discounts apply simultaneously
   - Edge case: `BilledAmount` at threshold boundary

## Acceptance Criteria
- [ ] Discount never exceeds `MaxAdjustmentsAllowed`
- [ ] Business rule intent is documented in code comments
- [ ] Unit tests cover all discount scenarios
""",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # CODE QUALITY
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "[Refactor] Add dependency injection for BusinessRuleRequestHandler and factory",
        "labels": ["refactor", "architecture"],
        "body": """\
## Summary
`BusinessRuleController` creates `BusinessRuleRequestHandler` directly with `new`, bypassing ASP.NET Core's DI container. This makes the controller untestable and tightly coupled.

## Current Code
```csharp
// BusinessRuleController.cs
var handler = new BusinessRuleRequestHandler();  // ← direct instantiation

// BusinessRuleRequestHandler.cs
var factory = new RuleEngineFactory();            // ← direct instantiation
var ruleExecutor = new BusinessRuleExecutor();   // ← direct instantiation
```

## Target Architecture
```csharp
// Startup.cs / Program.cs
services.AddScoped<IRequestHandler, BusinessRuleRequestHandler>();
services.AddScoped<IRuleEngineFactory, RuleEngineFactory>();
services.AddScoped<IRuleExecutor, BusinessRuleExecutor>();

// BusinessRuleController.cs
public BusinessRuleController(IRequestHandler handler)
{
    _handler = handler;
}
```

## Implementation Steps
1. Register `IRequestHandler`, `IRuleEngineFactory`, and `IRuleExecutor` in `Startup.cs` (or `Program.cs`).
2. Update `BusinessRuleController` constructor to accept `IRequestHandler` via DI.
3. Update `BusinessRuleRequestHandler` constructor to accept `IRuleEngineFactory` and `IRuleExecutor` via DI.
4. Verify the DI chain resolves correctly at startup.

## Acceptance Criteria
- [ ] No `new` instantiation of handlers/factories in controllers or handlers
- [ ] All dependencies registered in DI container
- [ ] Controller tested with a mocked `IRequestHandler`
""",
    },
    {
        "title": "[Refactor] Replace Console.Write with ILogger for structured logging",
        "labels": ["refactor", "observability"],
        "body": """\
## Summary
`BusinessRuleRequestHandler.cs` uses `Console.Write` to output rule execution logs. This is not suitable for production — it cannot be filtered, routed to centralized logging, or correlated with request tracing.

## Location
`BusinessRuleDomain/RuleRequestHandler/BusinessRuleRequestHandler.cs`, lines 25-26

## Current Code
```csharp
string json = JsonConvert.SerializeObject(ruleExecutor.Logs, Formatting.Indented);
Console.Write(json);
```

## Fix
Inject `ILogger<BusinessRuleRequestHandler>` and use structured logging:
```csharp
public class BusinessRuleRequestHandler : IRequestHandler
{
    private readonly ILogger<BusinessRuleRequestHandler> _logger;

    public BusinessRuleRequestHandler(ILogger<BusinessRuleRequestHandler> logger)
    {
        _logger = logger;
    }

    public async Task<IRuleEngineResult> Handle(RuleRequest request)
    {
        // ...
        _logger.LogInformation("Rule execution completed. Logs: {@Logs}", ruleExecutor.Logs);
        // ...
    }
}
```

## Implementation Steps
1. Add `Microsoft.Extensions.Logging.Abstractions` dependency to `BusinessRuleDomain.csproj` if not already available.
2. Inject `ILogger<BusinessRuleRequestHandler>` in constructor.
3. Replace `Console.Write(json)` with `_logger.LogInformation(...)`.
4. Register logger in DI (already done by `AddLogging()` in `Startup.cs`).

## Acceptance Criteria
- [ ] No `Console.Write` / `Console.WriteLine` in production code paths
- [ ] Structured logging with `ILogger` used throughout
- [ ] Logs are visible via standard ASP.NET Core logging pipeline
""",
    },
    {
        "title": "[Refactor] Add input validation and error handling to BusinessRuleController",
        "labels": ["refactor", "security"],
        "body": """\
## Summary
`BusinessRuleController.Execute()` has no input validation and no error handling. An invalid `RuleName`, null `Input`, or unregistered rule will throw an unhandled exception, returning a 500 with a stack trace.

## Current Code
```csharp
public IActionResult Execute([FromBody] RuleRequest request)
{
    var handler = new BusinessRuleRequestHandler();
    return Ok(handler.Handle(request).Result);  // throws on invalid input
}
```

## Fix
```csharp
[HttpPost]
public async Task<IActionResult> Execute([FromBody] RuleRequest request)
{
    if (request is null)
        return BadRequest("Request body is required.");

    if (string.IsNullOrWhiteSpace(request.RuleName))
        return BadRequest("RuleName is required.");

    if (request.Input is null)
        return BadRequest("Input is required.");

    try
    {
        var result = await _handler.Handle(request);
        return Ok(result);
    }
    catch (KeyNotFoundException ex)
    {
        return NotFound($"Rule '{request.RuleName}' not found.");
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error executing rule '{RuleName}'", request.RuleName);
        return StatusCode(500, "An error occurred while executing the rule.");
    }
}
```

## Implementation Steps
1. Add null checks for `request`, `request.RuleName`, and `request.Input`.
2. Wrap execution in try/catch:
   - `KeyNotFoundException` → 404 Not Found
   - General `Exception` → 500 with logged error, no stack trace in response
3. Add `[Required]` data annotations to `RuleRequest` model properties.
4. Add `ModelState.IsValid` check (or use `[ApiController]` automatic validation).
5. Inject `ILogger<BusinessRuleController>`.

## Acceptance Criteria
- [ ] Null request returns 400
- [ ] Unknown `RuleName` returns 404
- [ ] Internal errors return 500 without exposing stack traces
- [ ] All validation errors return 400 with descriptive message
- [ ] Errors are logged with appropriate level
""",
    },
    {
        "title": "[Cleanup] Remove unused Class1.cs placeholder file",
        "labels": ["cleanup"],
        "body": """\
## Summary
`BusinessRuleDomain/Class1.cs` is an empty placeholder file generated by the .NET project template. It serves no purpose and adds noise.

## Location
`BusinessRuleDomain/Class1.cs`

## Current Content
```csharp
using System;

namespace BusinessRuleDomain
{
    public class Class1
    {
    }
}
```

## Implementation Steps
1. Delete `BusinessRuleDomain/Class1.cs`.
2. Verify build still succeeds.

## Acceptance Criteria
- [ ] `Class1.cs` deleted
- [ ] Build succeeds
""",
    },
    {
        "title": "[Cleanup] Add graceful error handling to RuleEngineFactory for unknown rule names",
        "labels": ["cleanup", "bug"],
        "body": """\
## Summary
`RuleEngineFactory.GetRuleEngine()` and `GetRuleEngineFact()` use raw dictionary lookups that throw `KeyNotFoundException` when an unregistered rule name is provided. This exception propagates to the API caller as an unhandled 500.

## Location
`BusinessRuleDomain/RuleRequestHandler/RuleEngineFactory.cs`, lines 24-26

## Current Code
```csharp
public IRuleEngine GetRuleEngine(string ruleName) => _engines[ruleName];     // throws KeyNotFoundException
public IRuleEngineFacts GetRuleEngineFact(string ruleName) => _facts[ruleName]; // throws KeyNotFoundException
```

## Fix
```csharp
public IRuleEngine GetRuleEngine(string ruleName)
{
    if (!_engines.TryGetValue(ruleName, out var engine))
        throw new ArgumentException($"Rule engine '{ruleName}' is not registered. Available: {string.Join(", ", _engines.Keys)}");
    return engine;
}

public IRuleEngineFacts GetRuleEngineFact(string ruleName)
{
    if (!_facts.TryGetValue(ruleName, out var facts))
        throw new ArgumentException($"Rule facts for '{ruleName}' are not registered. Available: {string.Join(", ", _facts.Keys)}");
    return facts;
}
```
And in the controller: catch `ArgumentException` → return 400 Bad Request.

## Implementation Steps
1. Replace raw dictionary index access with `TryGetValue`.
2. Throw `ArgumentException` (not `KeyNotFoundException`) with a descriptive message listing available rules.
3. Update controller error handling (see related issue) to catch `ArgumentException` → 400.

## Acceptance Criteria
- [ ] Unknown rule name returns 400 with list of valid rule names
- [ ] No `KeyNotFoundException` escapes to the caller
""",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TESTING
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "[Testing] Add unit test project for BusinessRuleDomain",
        "labels": ["testing"],
        "body": """\
## Summary
The repository has **zero tests**. Add a dedicated xUnit test project covering the core business logic.

## Implementation Steps

### 1. Create the test project
```bash
dotnet new xunit -n BusinessRuleDomain.Tests
dotnet sln add BusinessRuleDomain.Tests/BusinessRuleDomain.Tests.csproj
```

### 2. Add dependencies
```xml
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
<PackageReference Include="Moq" Version="4.20.72" />
<PackageReference Include="FluentAssertions" Version="6.12.2" />
```

### 3. Required test cases

#### `DiscountEngineTests`
| Test | Scenario | Expected |
|---|---|---|
| `FirstTimeCustomer_GetsDiscount` | `PurchaseCount == 0` | 10% discount applied |
| `FrequentCustomer_GetsDiscount` | `PurchaseCount >= 10` | 7% discount applied |
| `BulkPurchase_GetsDiscount` | `BilledAmount >= 10000` | 10% discount applied |
| `NoRuleMatches_NoDiscount` | `PurchaseCount = 5, BilledAmount = 500` | 0% discount |
| `MultipleRulesMatch_DiscountCapped` | All three rules match | Total ≤ MaxAdjustmentsAllowed |
| `BoundaryConditions` | `PurchaseCount == 9`, `BilledAmount == 9999` | No frequent/bulk discount |

#### `BusinessRuleExecutorTests`
- Verify rule logs are populated after execution
- Verify log contains correct `RuleName`, `Result`, and `Timestamp`

#### `RuleEngineFactoryTests`
- `GetRuleEngine("DiscountEngine")` returns `DiscountEngine` instance
- `GetRuleEngine("Unknown")` throws `ArgumentException` with available rules listed

#### `BusinessRuleRequestHandlerTests` (integration-style)
- Valid `DiscountEngine` request → returns result with applied discounts
- Invalid rule name → propagates error correctly

## Acceptance Criteria
- [ ] Test project created and included in solution
- [ ] All `DiscountEngine` scenarios covered
- [ ] `RuleEngineFactory` error cases tested
- [ ] All tests pass with `dotnet test`
- [ ] Code coverage ≥ 80% for `BusinessRuleDomain`
""",
    },
    {
        "title": "[Testing] Add integration tests for BusinessRulesApi endpoints",
        "labels": ["testing"],
        "body": """\
## Summary
Add integration tests using `Microsoft.AspNetCore.Mvc.Testing` to test the full HTTP request/response cycle.

## Implementation Steps

### 1. Create the test project
```bash
dotnet new xunit -n BusinessRulesApi.Tests
dotnet sln add BusinessRulesApi.Tests/BusinessRulesApi.Tests.csproj
```

### 2. Add dependencies
```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="10.0.x" />
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="FluentAssertions" Version="6.12.2" />
```

### 3. Required test cases

#### `BusinessRuleControllerIntegrationTests`
| Test | Input | Expected HTTP Status |
|---|---|---|
| `ValidDiscountRequest_Returns200` | Valid `CustomerInfo` JSON | 200 OK with discount result |
| `NullBody_Returns400` | Empty body | 400 Bad Request |
| `EmptyRuleName_Returns400` | `RuleName: ""` | 400 Bad Request |
| `UnknownRuleName_Returns404` | `RuleName: "Unknown"` | 404 Not Found |
| `MalformedInput_Returns400` | `Input` field with wrong types | 400 Bad Request |

### 4. Sample test
```csharp
[Fact]
public async Task ValidDiscountRequest_Returns200WithResult()
{
    var client = _factory.CreateClient();
    var payload = new
    {
        requestId = Guid.NewGuid(),
        workflowIdentifier = Guid.NewGuid(),
        ruleName = "DiscountEngine",
        input = new { name = "Alice", age = 30, purchaseCount = 0, billedAmount = 500 }
    };

    var response = await client.PostAsJsonAsync("/v1/businessrule", payload);

    response.StatusCode.Should().Be(HttpStatusCode.OK);
    var result = await response.Content.ReadFromJsonAsync<DiscountEngineResult>();
    result.Should().NotBeNull();
}
```

## Acceptance Criteria
- [ ] Integration test project created
- [ ] Happy path test passes
- [ ] All error cases return correct HTTP status codes
- [ ] Tests run with `dotnet test`
""",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # DOCUMENTATION
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "[Docs] Write README.md with project overview, setup, and usage guide",
        "labels": ["documentation"],
        "body": """\
## Summary
`README.md` is **completely empty**. Add comprehensive documentation.

## Required Sections

### 1. Project Overview
- What the BusinessRulesApp does
- Architecture overview (API layer + Domain layer)
- Supported rule engines (currently: `DiscountEngine`)

### 2. Prerequisites
- .NET 10 SDK
- (Optional) MongoDB if IAggregateDocument is implemented

### 3. Getting Started
```bash
git clone https://github.com/ShirasHassan/BusinessRulesApp
cd BusinessRulesApp
dotnet restore
dotnet build
dotnet run --project BusinessRulesApi
```

### 4. API Usage
**POST** `/v1/businessrule`

Request:
```json
{
  "requestId": "550e8400-e29b-41d4-a716-446655440000",
  "workflowIdentifier": "660e8400-e29b-41d4-a716-446655440001",
  "ruleName": "DiscountEngine",
  "input": {
    "name": "Alice",
    "age": 30,
    "purchaseCount": 0,
    "billedAmount": 500.00
  }
}
```

Response:
```json
{
  "discounts": [
    { "policyName": "FirstTimeCustomerPolicy", "discountPercent": 10 }
  ],
  "totalDiscount": 10
}
```

### 5. Adding New Rule Engines
Step-by-step guide for adding a custom rule engine.

### 6. Running Tests
```bash
dotnet test
```

### 7. Configuration
Document `appsettings.json` settings.

## Acceptance Criteria
- [ ] README.md has all sections listed above
- [ ] Code samples are accurate and tested
- [ ] Setup instructions work on a clean machine
""",
    },
    {
        "title": "[Security] Remove hardcoded personal email from appsettings.json",
        "labels": ["security", "cleanup"],
        "body": """\
## Summary
`appsettings.json` contains a hardcoded personal email address in the Swagger contact configuration:

```json
"Contact": {
  "Email": "shiras.hassan@gmail.com"
}
```

This should be replaced with a placeholder or configuration-driven value.

## Location
`BusinessRulesApi/appsettings.json`

## Fix Options
1. **Use a placeholder**: Replace with `"support@example.com"` or `"your-email@example.com"`.
2. **Environment variable**:
   ```json
   "Contact": {
     "Email": ""
   }
   ```
   And read from `SWAGGER_CONTACT_EMAIL` env var in `SwaggerSettings.cs`.
3. **Remove contact info entirely** if not needed in the OpenAPI spec.

## Implementation Steps
1. Replace the email in `appsettings.json`.
2. Verify Swagger UI does not expose personal contact information.

## Acceptance Criteria
- [ ] No personal email address in any committed file
- [ ] Swagger contact info uses a placeholder or is removed
""",
    },
    {
        "title": "[Performance] Cache compiled rule expressions in BusinessRule",
        "labels": ["performance"],
        "body": """\
## Summary
`BusinessRule<TFacts>` compiles its expression delegate on every call. With many concurrent requests, this is wasteful CPU usage. Compiled expressions should be cached.

## Location
`BusinessRuleDomain/RuleEngine/BusinessRule.cs`

## Current Code
```csharp
public bool Evaluate(TFacts facts)
{
    var compiled = Expression.Compile();  // recompiled on every call
    return compiled(facts);
}
```

## Fix — Static Cached Delegate per Rule Instance
Since `BusinessRule` is constructed once per rule engine (which is now DI-scoped), the compiled delegate should be lazily compiled and stored:

```csharp
public class BusinessRule<TFacts> : IRule<TFacts>
{
    private readonly Expression<Func<TFacts, bool>> _expression;
    private Func<TFacts, bool>? _compiledExpression;

    public BusinessRule(string name, Expression<Func<TFacts, bool>> expression)
    {
        Name = name;
        _expression = expression;
    }

    public bool Evaluate(TFacts facts)
    {
        _compiledExpression ??= _expression.Compile();
        return _compiledExpression(facts);
    }
}
```

## Implementation Steps
1. Add a `Func<TFacts, bool>? _compiledExpression` field.
2. Use `??=` lazy initialization in `Evaluate()`.
3. Load test to verify reduction in CPU usage.

## Acceptance Criteria
- [ ] Expression compiled only once per `BusinessRule` instance
- [ ] Thread-safe initialization (use `Lazy<T>` if multi-threaded concerns)
- [ ] Benchmark shows improved throughput under load
""",
    },
]


def create_issues(token: str) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    proxy = os.environ.get("GLOBAL_AGENT_HTTP_PROXY", "")
    proxies = {"http": proxy, "https": proxy} if proxy else {}

    # Ensure labels exist
    existing_labels = set()
    resp = requests.get(
        f"{API_BASE}/repos/{REPO}/labels",
        headers=headers,
        proxies=proxies,
        timeout=15,
    )
    if resp.status_code == 200:
        existing_labels = {l["name"] for l in resp.json()}

    needed_labels = {
        "upgrade": "0075ca",
        "bug": "d73a4a",
        "refactor": "e4e669",
        "cleanup": "ffffff",
        "testing": "0e8a16",
        "documentation": "0075ca",
        "security": "ee0701",
        "performance": "fbca04",
        "architecture": "c2e0c6",
        "async": "bfd4f2",
        "business-logic": "f9d0c4",
        "observability": "bfd4f2",
        "breaking-change": "b60205",
    }

    for label, color in needed_labels.items():
        if label not in existing_labels:
            r = requests.post(
                f"{API_BASE}/repos/{REPO}/labels",
                headers=headers,
                proxies=proxies,
                json={"name": label, "color": color},
                timeout=15,
            )
            if r.status_code == 201:
                print(f"  ✓ Created label: {label}")
            else:
                print(f"  ⚠ Could not create label '{label}': {r.status_code}")

    # Create issues
    created = 0
    for i, issue in enumerate(ISSUES, 1):
        print(f"\n[{i}/{len(ISSUES)}] Creating: {issue['title']}")
        resp = requests.post(
            f"{API_BASE}/repos/{REPO}/issues",
            headers=headers,
            proxies=proxies,
            json=issue,
            timeout=15,
        )
        if resp.status_code == 201:
            data = resp.json()
            print(f"  ✓ Created #{data['number']}: {data['html_url']}")
            created += 1
        else:
            print(f"  ✗ Failed ({resp.status_code}): {resp.text[:200]}")

        if i < len(ISSUES):
            time.sleep(0.5)  # avoid secondary rate limits

    print(f"\n\nDone: {created}/{len(ISSUES)} issues created.")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ERROR: Set GITHUB_TOKEN environment variable.")
        print("  export GITHUB_TOKEN=ghp_your_token_here")
        print("  python3 create_github_issues.py")
        sys.exit(1)

    print(f"Creating {len(ISSUES)} issues on {REPO}...\n")
    create_issues(token)

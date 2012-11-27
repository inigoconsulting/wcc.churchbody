
        # Integration tests for ChurchBody
        ztc.ZopeDocFileSuite(
            'ChurchBody.txt',
            package='wcc.churchbody',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


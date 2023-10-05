# ***pybn***

    Python package for simple build number generation.

    Make sure to have the latest version of Python 3 installed although this should work with previous versions. 

    To install the package with pip enter command in terminal:
        pip install pybn

    To uninstall the package with pip enter command in terminal:
        pip uninstall pybn

<table width="100%">
	<tr>
		<th align="left">
            Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
	<tr>
		<td>
            <code>generate_buildnumber(current_build_number = None, limit = 100)</code>
        </td>
		<td>
            Generates a new build number from an existing build number if provided in the current_build_number argument.
            Build numbers are in the following format: 'xxx.xxx.xxx'
            The limit argument is the highest number the back two segments of the build number can be before shifting over (Set to 100 by default).
        </td>
	</tr>
</table>

[Back to Top](#pybn)

---
